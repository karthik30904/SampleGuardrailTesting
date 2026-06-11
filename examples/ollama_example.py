"""Example showing how to use the Ollama provider with the toxicity guardrail."""

from __future__ import annotations

from agent_guardrails.guardrails.output.toxicity import ToxicityGuardrail
from agent_guardrails.providers.ollama_provider import OllamaProvider, OllamaProviderError


def main() -> None:
    """Run a toxicity check against a local Ollama server."""

    provider = OllamaProvider(model="llama3.1")
    guardrail = ToxicityGuardrail(provider=provider)
    try:
        result = guardrail.validate("You are a helpful assistant.")
        print(result)
    except OllamaProviderError as exc:
        print(f"Ollama request failed: {exc}")


if __name__ == "__main__":
    main()

