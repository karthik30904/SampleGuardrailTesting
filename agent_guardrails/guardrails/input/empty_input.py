"""Guardrail that blocks empty or whitespace-only input."""

from __future__ import annotations

from dataclasses import dataclass

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class EmptyInputGuardrail(BaseGuardrail):
    """Block requests that do not contain meaningful text."""

    name: str = "EmptyInputGuardrail"

    def validate(self, text: str) -> GuardrailResult:
        """Return a failure result when the input is empty."""

        if text.strip():
            return GuardrailResult(True, "Input is not empty.", self.name)
        return GuardrailResult(False, "Input is empty or whitespace only.", self.name)

