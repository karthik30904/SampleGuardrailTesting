"""LLM-backed guardrail that classifies output toxicity."""

from __future__ import annotations

from dataclasses import dataclass

from agent_guardrails.guardrails.base import BaseGuardrail
from agent_guardrails.models.result import GuardrailResult
from agent_guardrails.providers.base import BaseProvider


@dataclass(slots=True)
class ToxicityGuardrail(BaseGuardrail):
    """Use a provider-backed model to classify output toxicity."""

    provider: BaseProvider
    name: str = "ToxicityGuardrail"

    def validate(self, text: str) -> GuardrailResult:
        """Ask the provider to classify the text as SAFE or TOXIC."""

        prompt = (
            "Classify the following assistant output as SAFE or TOXIC.\n"
            "Return exactly one word: SAFE or TOXIC.\n\n"
            f"Output:\n{text}"
        )
        response = self.provider.generate(prompt).strip().upper()
        if "TOXIC" in response and "SAFE" not in response:
            return GuardrailResult(False, "LLM classified the output as toxic.", self.name)
        if response.startswith("SAFE") or response == "SAFE":
            return GuardrailResult(True, "LLM classified the output as safe.", self.name)
        return GuardrailResult(
            False,
            f"Unable to parse toxicity classification from provider response: {response}",
            self.name,
        )

