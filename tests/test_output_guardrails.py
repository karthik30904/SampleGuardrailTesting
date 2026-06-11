"""Tests for output guardrails."""

from __future__ import annotations

from agent_guardrails.guardrails.output.output_length import OutputLengthGuardrail
from agent_guardrails.guardrails.output.sensitive_output import SensitiveOutputGuardrail
from agent_guardrails.guardrails.output.toxicity import ToxicityGuardrail


def test_sensitive_output_guardrail_blocks_secret() -> None:
    """Secret-like output should be rejected."""

    result = SensitiveOutputGuardrail().validate("api_key = sk-1234567890abcdef1234")
    assert result.allowed is False


def test_sensitive_output_guardrail_allows_safe_output() -> None:
    """Ordinary output should pass."""

    result = SensitiveOutputGuardrail().validate("This is a normal response.")
    assert result.allowed is True


def test_toxicity_guardrail_blocks_toxic_output(toxic_provider) -> None:
    """LLM toxicity classification should block toxic content."""

    guardrail = ToxicityGuardrail(provider=toxic_provider)
    result = guardrail.validate("mean and harmful text")
    assert result.allowed is False
    assert toxic_provider.prompts


def test_toxicity_guardrail_allows_safe_output(safe_provider) -> None:
    """LLM toxicity classification should allow safe content."""

    guardrail = ToxicityGuardrail(provider=safe_provider)
    result = guardrail.validate("kind and helpful text")
    assert result.allowed is True
    assert safe_provider.prompts


def test_output_length_guardrail_blocks_long_output() -> None:
    """Output above the configured length should fail."""

    result = OutputLengthGuardrail(max_length=3).validate("long")
    assert result.allowed is False


def test_output_length_guardrail_allows_short_output() -> None:
    """Short output should pass the length guardrail."""

    result = OutputLengthGuardrail(max_length=10).validate("ok")
    assert result.allowed is True

