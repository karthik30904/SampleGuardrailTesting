"""Guardrail that enforces a maximum output length."""

from __future__ import annotations

from dataclasses import dataclass

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class OutputLengthGuardrail(BaseGuardrail):
    """Block output that exceeds the configured length."""

    max_length: int
    name: str = "OutputLengthGuardrail"

    def validate(self, text: str) -> GuardrailResult:
        """Check whether the output length is within the configured limit."""

        if len(text) <= self.max_length:
            return GuardrailResult(True, "Output length is within the limit.", self.name)
        return GuardrailResult(
            False,
            f"Output length {len(text)} exceeds maximum length {self.max_length}.",
            self.name,
        )

