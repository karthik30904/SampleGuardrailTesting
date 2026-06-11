"""Example showing how an agent can combine input and output guardrails."""

from __future__ import annotations

from dataclasses import dataclass

from agent_guardrails.engine.guardrail_engine import GuardrailEngine
from agent_guardrails.guardrails.input.empty_input import EmptyInputGuardrail
from agent_guardrails.guardrails.input.keyword_block import KeywordBlockGuardrail
from agent_guardrails.guardrails.input.pii_detection import PIIDetectionGuardrail
from agent_guardrails.guardrails.output.output_length import OutputLengthGuardrail
from agent_guardrails.guardrails.output.sensitive_output import SensitiveOutputGuardrail


@dataclass(slots=True)
class EchoAgent:
    """A tiny example agent that echoes user input."""

    engine: GuardrailEngine

    def run(self, user_input: str) -> str:
        """Validate input, generate output, then validate output."""

        input_result = self.engine.validate_input(user_input)
        if not input_result.allowed:
            return f"Blocked input: {input_result.reason}"

        response = f"Assistant response to: {user_input}"
        output_result = self.engine.validate_output(response)
        if not output_result.allowed:
            return f"Blocked output: {output_result.reason}"

        return response


def main() -> None:
    """Demonstrate the full agent flow."""

    engine = GuardrailEngine(
        input_guardrails=[EmptyInputGuardrail(), KeywordBlockGuardrail(keywords=["forbidden"]), PIIDetectionGuardrail()],
        output_guardrails=[SensitiveOutputGuardrail(), OutputLengthGuardrail(max_length=500)],
    )
    agent = EchoAgent(engine=engine)
    print(agent.run("Hello, guardrails."))


if __name__ == "__main__":
    main()

