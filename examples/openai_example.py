"""Example showing how to use the OpenAI provider with the toxicity guardrail."""

from __future__ import annotations

import os

from agent_guardrails.guardrails.output.toxicity import ToxicityGuardrail
from agent_guardrails.providers.openai_provider import OpenAIProvider, OpenAIProviderError


def main() -> None:
    """Run a toxicity check against OpenAI if credentials are configured."""

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("Set OPENAI_API_KEY to run this example.")
        return

    provider = OpenAIProvider(api_key=api_key)
    guardrail = ToxicityGuardrail(provider=provider)
    try:
        result = guardrail.validate("You are a helpful assistant.")
        print(result)
    except OpenAIProviderError as exc:
        print(f"OpenAI request failed: {exc}")


if __name__ == "__main__":
    main()

