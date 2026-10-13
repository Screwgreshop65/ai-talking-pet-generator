"""LLM backend abstraction with a deterministic offline fallback."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from petgen.models.config_model import LLMServiceConfig
from petgen.models.pet_profile import Persona


@dataclass(frozen=True, slots=True)
class LLMResponse:
    emotion: str
    reply: str


class LLMBackend(Protocol):
    async def classify(self, text: str, labels: list[str]) -> str: ...
    async def respond(self, *, persona: Persona, user_text: str, intent: str) -> LLMResponse: ...


class EchoBackend:
    """Offline fallback. Deterministic; used when no remote backend is configured."""

    async def classify(self, text: str, labels: list[str]) -> str:
        lowered = text.lower()
        if any(w in lowered for w in ("hi", "hello", "hey")):
            return "greet"
        if text.endswith("?"):
            return "question"
        return "chatter"

    async def respond(self, *, persona: Persona, user_text: str, intent: str) -> LLMResponse:
        emotion = "curious" if intent == "question" else "happy"
        return LLMResponse(emotion=emotion, reply=f"{persona.catchphrase} {user_text}".strip())


def get_llm_backend(config: LLMServiceConfig) -> LLMBackend:
    """Resolve the backend named in config. Falls back to EchoBackend."""
    if config.backend == "openai_compatible" and config.base_url:
        from petgen.services.llm_openai import OpenAICompatibleBackend

        return OpenAICompatibleBackend(config)
    if config.backend == "local_gguf" and config.model_path:
        from petgen.services.llm_local import LocalGGUFBackend

        return LocalGGUFBackend(config)
    return EchoBackend()