"""Engine that executes registered input and output guardrails."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.logging.logger import get_logger
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class GuardrailEngine:
    """Run guardrails in order and stop on the first failure."""

    input_guardrails: list[BaseGuardrail] = field(default_factory=list)
    output_guardrails: list[BaseGuardrail] = field(default_factory=list)

    def register_input_guardrail(self, guardrail: BaseGuardrail) -> None:
        """Add an input guardrail to the execution chain."""

        self.input_guardrails.append(guardrail)

    def register_output_guardrail(self, guardrail: BaseGuardrail) -> None:
        """Add an output guardrail to the execution chain."""

        self.output_guardrails.append(guardrail)

    def register_input_guardrails(self, guardrails: Sequence[BaseGuardrail]) -> None:
        """Add multiple input guardrails to the execution chain."""

        self.input_guardrails.extend(guardrails)

    def register_output_guardrails(self, guardrails: Sequence[BaseGuardrail]) -> None:
        """Add multiple output guardrails to the execution chain."""

        self.output_guardrails.extend(guardrails)

    def validate_input(self, text: str) -> GuardrailResult:
        """Validate input text with the registered input guardrails."""

        return self._validate(text, self.input_guardrails, "input")

    def validate_output(self, text: str) -> GuardrailResult:
        """Validate output text with the registered output guardrails."""

        return self._validate(text, self.output_guardrails, "output")

    def _validate(
        self,
        text: str,
        guardrails: Sequence[BaseGuardrail],
        direction: str,
    ) -> GuardrailResult:
        """Run guardrails in order and return the first failure or success."""

        logger = get_logger()
        for guardrail in guardrails:
            logger.info("Running %s", guardrail.name)
            result = guardrail.validate(text)
            if result.allowed:
                logger.info("%s passed", guardrail.name)
                continue
            logger.warning("%s blocked %s", guardrail.name, f"{direction} request" if direction == "input" else "response")
            logger.warning("%s", result.reason)
            return result

        return GuardrailResult(
            True,
            f"All {direction} guardrails passed.",
            "GuardrailEngine",
        )

