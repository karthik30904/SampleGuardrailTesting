"""OpenAI provider implementation using the Chat Completions HTTP API."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from agent_guardrails.providers.base import BaseProvider


class OpenAIProviderError(RuntimeError):
    """Raised when the OpenAI provider cannot produce a response."""


@dataclass(slots=True)
class OpenAIProvider(BaseProvider):
    """Generate text with OpenAI's HTTP API."""

    api_key: str
    model: str = "gpt-4o-mini"
    base_url: str = "https://api.openai.com/v1"
    timeout: float = 30.0

    def generate(self, prompt: str) -> str:
        """Send a prompt to OpenAI and return the first assistant message."""

        if not self.api_key.strip():
            raise OpenAIProviderError("OpenAI API key is required.")

        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a precise classification engine."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except error.URLError as exc:  # pragma: no cover - network failure path
            raise OpenAIProviderError(f"OpenAI request failed: {exc}") from exc

        payload = self._parse_json(raw)
        choices = payload.get("choices", [])
        if not choices:
            raise OpenAIProviderError("OpenAI response did not include choices.")

        message = choices[0].get("message", {})
        content = message.get("content", "")
        if not isinstance(content, str) or not content.strip():
            raise OpenAIProviderError("OpenAI response did not include text content.")
        return content.strip()

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        """Parse a JSON response body."""

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise OpenAIProviderError("OpenAI response was not valid JSON.") from exc

        if not isinstance(payload, dict):
            raise OpenAIProviderError("OpenAI response was not a JSON object.")
        return payload

