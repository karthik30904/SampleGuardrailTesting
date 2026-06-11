"""Example showing how to run output guardrails."""

from __future__ import annotations

from agent_guardrails.engine.guardrail_engine import GuardrailEngine
from agent_guardrails.guardrails.output.output_length import OutputLengthGuardrail
from agent_guardrails.guardrails.output.sensitive_output import SensitiveOutputGuardrail


def main() -> None:
    """Run a small output-validation demo."""

    engine = GuardrailEngine(
        output_guardrails=[
            SensitiveOutputGuardrail(),
            OutputLengthGuardrail(max_length=200),
        ]
    )
    result = engine.validate_output("Here is a short and safe answer.")
    print(result)


if __name__ == "__main__":
    main()

