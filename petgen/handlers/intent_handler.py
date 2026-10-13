"""Classify the user's intent so downstream stages can route."""

from __future__ import annotations

from petgen.models.config_model import AppConfig
from petgen.models.turn import Turn
from petgen.services.llm_backend import get_llm_backend

_INTENTS = {"greet", "question", "command", "chatter", "unknown"}


class IntentHandler:
    name = "intent"

    async def handle(self, turn: Turn, config: AppConfig) -> Turn:
        llm = get_llm_backend(config.services.llm)
        raw = await llm.classify(turn.text, labels=sorted(_INTENTS))
        turn.intent = raw if raw in _INTENTS else "unknown"
        return turn