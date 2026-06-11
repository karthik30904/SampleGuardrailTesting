"""Guardrail that detects common forms of personally identifiable information."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Pattern

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class PIIDetectionGuardrail(BaseGuardrail):
    """Detect common PII patterns in input text."""

    name: str = "PIIDetectionGuardrail"
    patterns: dict[str, Pattern[str]] = field(
        default_factory=lambda: {
            "email address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
            "phone number": re.compile(
                r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b"
            ),
            "social security number": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "credit card number": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        }
    )

    def validate(self, text: str) -> GuardrailResult:
        """Check whether the text contains a supported PII pattern."""

        for label, pattern in self.patterns.items():
            if pattern.search(text):
                return GuardrailResult(False, f"Detected {label}.", self.name)
        return GuardrailResult(True, "No PII detected.", self.name)

