"""Pick an emotion + reply draft given intent and pet persona."""

from __future__ import annotations

from petgen.models.config_model import AppConfig
from petgen.models.turn import Turn
from petgen.services.llm_backend import get_llm_backend


class EmotionHandler:
    name = "emotion"

    async def handle(self, turn: Turn, config: AppConfig) -> Turn:
        llm = get_llm_backend(config.services.llm)
        persona = config.profile.persona
        result = await llm.respond(persona=persona, user_text=turn.text, intent=turn.intent)
        turn.emotion = result.emotion
        turn.reply = result.reply
        return turn