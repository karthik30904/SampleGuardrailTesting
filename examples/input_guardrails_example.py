"""Example showing how to run input guardrails."""

from __future__ import annotations

from agent_guardrails.engine.guardrail_engine import GuardrailEngine
from agent_guardrails.guardrails.input.empty_input import EmptyInputGuardrail
from agent_guardrails.guardrails.input.keyword_block import KeywordBlockGuardrail
from agent_guardrails.guardrails.input.max_length import MaxLengthGuardrail
from agent_guardrails.guardrails.input.pii_detection import PIIDetectionGuardrail
from agent_guardrails.guardrails.input.prompt_injection import PromptInjectionGuardrail


def main() -> None:
    """Run a small input-validation demo."""

    engine = GuardrailEngine(
        input_guardrails=[
            EmptyInputGuardrail(),
            KeywordBlockGuardrail(keywords=["forbidden", "secret"]),
            PIIDetectionGuardrail(),
            PromptInjectionGuardrail(),
            MaxLengthGuardrail(max_length=200),
        ]
    )
    result = engine.validate_input("Please summarize this harmless sentence.")
    print(result)


if __name__ == "__main__":
    main()

