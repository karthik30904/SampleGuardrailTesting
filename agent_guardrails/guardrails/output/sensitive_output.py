"""Guardrail that blocks output containing likely secrets or sensitive data."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Pattern

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class SensitiveOutputGuardrail(BaseGuardrail):
    """Detect output that appears to contain secret material or PII."""

    name: str = "SensitiveOutputGuardrail"
    patterns: dict[str, Pattern[str]] = field(
        default_factory=lambda: {
            "api key": re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
            "aws access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
            "github token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b", re.I),
            "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            "password disclosure": re.compile(r"\bpassword\s*[:=]\s*.+", re.I),
            "bearer token": re.compile(r"\bBearer\s+[A-Za-z0-9\-._~+/]+=*\b"),
            "social security number": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "credit card number": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        }
    )

    def validate(self, text: str) -> GuardrailResult:
        """Check whether the text contains a likely secret or sensitive value."""

        for label, pattern in self.patterns.items():
            if pattern.search(text):
                return GuardrailResult(False, f"Detected sensitive output: {label}.", self.name)
        return GuardrailResult(True, "No sensitive output detected.", self.name)

