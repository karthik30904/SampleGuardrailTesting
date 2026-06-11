"""Guardrail that flags prompt-injection style instructions."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Pattern

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class PromptInjectionGuardrail(BaseGuardrail):
    """Detect common prompt injection phrases and manipulation attempts."""

    name: str = "PromptInjectionGuardrail"
    patterns: dict[str, Pattern[str]] = field(
        default_factory=lambda: {
            "ignore previous instructions": re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
            "reveal system prompt": re.compile(r"(reveal|show|print).{0,20}(system prompt|developer prompt|hidden prompt)", re.I),
            "bypass safety": re.compile(r"(bypass|override|disable).{0,20}(safety|guardrail|policy|filter)", re.I),
            "developer mode": re.compile(r"developer\s+mode", re.I),
            "jailbreak": re.compile(r"jailbreak", re.I),
        }
    )

    def validate(self, text: str) -> GuardrailResult:
        """Check whether the text contains an injection attempt."""

        for label, pattern in self.patterns.items():
            if pattern.search(text):
                return GuardrailResult(False, f"Detected prompt injection pattern: {label}.", self.name)
        return GuardrailResult(True, "No prompt injection detected.", self.name)

