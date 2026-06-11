"""Ollama provider implementation using the local HTTP API."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from agent_guardrails.providers.base import BaseProvider


class OllamaProviderError(RuntimeError):
    """Raised when the Ollama provider cannot produce a response."""


@dataclass(slots=True)
class OllamaProvider(BaseProvider):
    """Generate text with a locally hosted Ollama server."""

    model: str = "llama3.1"
    base_url: str = "http://localhost:11434"
    timeout: float = 30.0

    def generate(self, prompt: str) -> str:
        """Send a prompt to Ollama and return the generated response text."""

        url = f"{self.base_url.rstrip('/')}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except error.URLError as exc:  # pragma: no cover - network failure path
            raise OllamaProviderError(f"Ollama request failed: {exc}") from exc

        payload = self._parse_json(raw)
        content = payload.get("response", "")
        if not isinstance(content, str) or not content.strip():
            raise OllamaProviderError("Ollama response did not include text content.")
        return content.strip()

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        """Parse a JSON response body."""

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise OllamaProviderError("Ollama response was not valid JSON.") from exc

        if not isinstance(payload, dict):
            raise OllamaProviderError("Ollama response was not a JSON object.")
        return payload

