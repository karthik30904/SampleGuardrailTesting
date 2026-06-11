"""Tests for the guardrail engine."""

from __future__ import annotations

from dataclasses import dataclass

from agent_guardrails.engine.guardrail_engine import GuardrailEngine
from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.guardrails.input.empty_input import EmptyInputGuardrail
from agent_guardrails.guardrails.input.keyword_block import KeywordBlockGuardrail
from agent_guardrails.guardrails.output.output_length import OutputLengthGuardrail
from agent_guardrails.models.result import GuardrailResult


@dataclass(slots=True)
class SpyGuardrail(BaseGuardrail):
    """Test helper that records validation calls."""

    name: str
    result: GuardrailResult
    calls: int = 0

    def validate(self, text: str) -> GuardrailResult:
        """Increment the call count and return the configured result."""

        self.calls += 1
        return self.result


def test_engine_allows_input_when_every_guardrail_passes() -> None:
    """The engine should allow input when all checks pass."""

    engine = GuardrailEngine()
    engine.register_input_guardrail(EmptyInputGuardrail())
    engine.register_input_guardrail(KeywordBlockGuardrail(keywords=["blocked"]))

    result = engine.validate_input("hello world")

    assert result.allowed is True
    assert result.guardrail_name == "GuardrailEngine"


def test_engine_stops_on_first_input_failure() -> None:
    """The engine should stop once a guardrail blocks input."""

    first = SpyGuardrail("First", GuardrailResult(False, "first blocked", "First"))
    second = SpyGuardrail("Second", GuardrailResult(True, "second passed", "Second"))
    engine = GuardrailEngine(input_guardrails=[first, second])

    result = engine.validate_input("input")

    assert result.allowed is False
    assert first.calls == 1
    assert second.calls == 0


def test_engine_allows_output_when_every_guardrail_passes() -> None:
    """The engine should allow output when all checks pass."""

    engine = GuardrailEngine()
    engine.register_output_guardrail(OutputLengthGuardrail(max_length=100))

    result = engine.validate_output("short output")

    assert result.allowed is True


def test_engine_stops_on_first_output_failure() -> None:
    """The engine should stop once a guardrail blocks output."""

    first = SpyGuardrail("First", GuardrailResult(False, "first blocked", "First"))
    second = SpyGuardrail("Second", GuardrailResult(True, "second passed", "Second"))
    engine = GuardrailEngine(output_guardrails=[first, second])

    result = engine.validate_output("output")

    assert result.allowed is False
    assert first.calls == 1
    assert second.calls == 0

