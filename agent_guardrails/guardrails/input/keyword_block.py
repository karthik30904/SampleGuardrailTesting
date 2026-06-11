"""Guardrail that blocks configured keywords in user input."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class KeywordBlockGuardrail(BaseGuardrail):
    """Block input containing one or more configured keywords."""

    keywords: Iterable[str] = field(default_factory=list)
    case_sensitive: bool = False
    name: str = "KeywordBlockGuardrail"

    def validate(self, text: str) -> GuardrailResult:
        """Check whether any blocked keyword is present in the text."""

        haystack = text if self.case_sensitive else text.lower()
        for keyword in self.keywords:
            needle = keyword if self.case_sensitive else keyword.lower()
            if needle and needle in haystack:
                return GuardrailResult(
                    False,
                    f"Blocked keyword detected: {keyword}",
                    self.name,
                )
        return GuardrailResult(True, "No blocked keywords detected.", self.name)

