"""Result models used across guardrail execution."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GuardrailResult:
    """Structured result returned by guardrails and the engine."""

    allowed: bool
    reason: str
    guardrail_name: str

