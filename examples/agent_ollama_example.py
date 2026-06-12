"""Single-file agent demo using `OllamaProvider` plus guardrails.

Before running this example:

1. Install the package in editable mode:
   `pip install -e .`
2. Start Ollama locally:
   `ollama serve`
3. Pull a model if needed:
   `ollama pull llama3.1`
4. Run the script:
   `python examples/agent_ollama_example.py`

This example shows how to:
- import `agent_guardrails` from another file
- use `OllamaProvider`
- wire input/output guardrails
- print step-by-step logs for the agent flow
"""

from __future__ import annotations

import ast
import operator as op
from dataclasses import dataclass

from agent_guardrails import (
    EmptyInputGuardrail,
    GuardrailEngine,
    KeywordBlockGuardrail,
    MaxLengthGuardrail,
    OllamaProvider,
    OutputLengthGuardrail,
    PIIDetectionGuardrail,
    PromptInjectionGuardrail,
    SensitiveOutputGuardrail,
    ToxicityGuardrail,
)
from agent_guardrails.logging.logger import get_logger


logger = get_logger()


_SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def calculator_tool(expression: str) -> str:
    """Safely evaluate a small arithmetic expression."""

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPERATORS:
            return _SAFE_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPERATORS:
            return _SAFE_OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Only simple arithmetic expressions are allowed.")

    tree = ast.parse(expression, mode="eval")
    result = _eval(tree.body)
    return str(int(result)) if result.is_integer() else str(result)


def knowledge_tool(topic: str) -> str:
    """Return a small canned knowledge snippet for demo purposes."""

    knowledge_base = {
        "guardrails": "Guardrails add safety checks before input reaches the model and before output reaches the user.",
        "ollama": "Ollama lets you run local models through a simple HTTP API.",
        "logging": "Logging helps you trace tool usage, guardrail decisions, and model responses.",
    }
    return knowledge_base.get(topic.lower().strip(), f"No knowledge entry found for '{topic}'.")


@dataclass(slots=True)
class OllamaAgent:
    """A tiny agent that uses Ollama for the final response."""

    engine: GuardrailEngine
    provider: OllamaProvider

    def run(self, user_input: str) -> str:
        logger.info("User input received: %s", user_input)

        input_result = self.engine.validate_input(user_input)
        logger.info("Input guardrail result: %s | allowed=%s", input_result.guardrail_name, input_result.allowed)
        logger.info("Input guardrail reason: %s", input_result.reason)
        if not input_result.allowed:
            return f"Blocked input: {input_result.reason}"

        tool_context = self._use_tools(user_input)