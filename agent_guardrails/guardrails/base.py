"""Base classes and shared helpers for guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from agent_guardrails.models.result import GuardrailResult


class BaseGuardrail(ABC):
    """Common interface for all guardrails."""

    name: str

    @abstractmethod
    def validate(self, text: str) -> GuardrailResult:
        """Validate the supplied text and return a structured result."""

