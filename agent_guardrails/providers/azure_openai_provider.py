"""Azure OpenAI provider implementation using the chat completions HTTP API."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from agent_guardrails.providers.base import BaseProvider


class AzureOpenAIProviderError(RuntimeError):
    """Raised when the Azure OpenAI provider cannot produce a response."""


@dataclass(slots=True)
class AzureOpenAIProvider(BaseProvider):
    """Generate text with Azure OpenAI's REST API.

    Parameters
    ----------
    api_key:
        Azure OpenAI resource key.
    endpoint:
        Base endpoint for the Azure OpenAI resource, for example
        ``https://my-resource.openai.azure.com``.
    deployment:
        The deployment name created in Azure OpenAI Studio.
    api_version:
        Azure OpenAI API version, for example ``2024-02-15-preview``.
    """

    api_key: str
    endpoint: str
    deployment: str
    api_version: str = "2024-02-15-preview"
    timeout: float = 30.0

    def generate(self, prompt: str) -> str:
        """Send a prompt to Azure OpenAI and return the assistant response."""

        if not self.api_key.strip():
            raise AzureOpenAIProviderError("Azure OpenAI API key is required.")
        if not self.endpoint.strip():
            raise AzureOpenAIProviderError("Azure OpenAI endpoint is required.")
        if not self.deployment.strip():
            raise AzureOpenAIProviderError("Azure OpenAI deployment is required.")

        url = (
            f"{self.endpoint.rstrip('/')}/openai/deployments/"
            f"{self.deployment}/chat/completions?api-version={self.api_version}"
        )
        payload = {
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
                "api-key": self.api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except error.URLError as exc:  # pragma: no cover - network failure path
            raise AzureOpenAIProviderError(f"Azure OpenAI request failed: {exc}") from exc

        payload = self._parse_json(raw)
        choices = payload.get("choices", [])
        if not choices:
            raise AzureOpenAIProviderError("Azure OpenAI response did not include choices.")

        message = choices[0].get("message", {})
        content = message.get("content", "")
        if not isinstance(content, str) or not content.strip():
            raise AzureOpenAIProviderError("Azure OpenAI response did not include text content.")
        return content.strip()

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        """Parse a JSON response body."""

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AzureOpenAIProviderError("Azure OpenAI response was not valid JSON.") from exc

        if not isinstance(payload, dict):
            raise AzureOpenAIProviderError("Azure OpenAI response was not a JSON object.")
        return payload
