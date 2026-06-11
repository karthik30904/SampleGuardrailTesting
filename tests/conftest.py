"""Pytest fixtures for the agent guardrails test suite."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from agent_guardrails.providers.base import BaseProvider


class DummyProvider(BaseProvider):
    """A deterministic provider for tests."""

    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


@pytest.fixture()
def safe_provider() -> Iterator[DummyProvider]:
    """Yield a provider that classifies everything as safe."""

    yield DummyProvider("SAFE")


@pytest.fixture()
def toxic_provider() -> Iterator[DummyProvider]:
    """Yield a provider that classifies everything as toxic."""

    yield DummyProvider("TOXIC")

