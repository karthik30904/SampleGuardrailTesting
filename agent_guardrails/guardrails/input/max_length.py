"""Guardrail that enforces a maximum input length."""

from __future__ import annotations

from dataclasses import dataclass

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class MaxLengthGuardrail(BaseGuardrail):
    """Block input that exceeds the configured length."""

    max_length: int
    name: str = "MaxLengthGuardrail"

    def validate(self, text: str) -> GuardrailResult:
        """Check whether the input length is within the configured limit."""

        if len(text) <= self.max_length:
            return GuardrailResult(True, "Input length is within the limit.", self.name)
        return GuardrailResult(
            False,
            f"Input length {len(text)} exceeds maximum length {self.max_length}.",
            self.name,
        )

