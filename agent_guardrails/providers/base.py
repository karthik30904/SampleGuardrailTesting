"""Provider abstraction for LLM-backed guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Base abstraction for text-generation providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a textual response for the provided prompt."""

