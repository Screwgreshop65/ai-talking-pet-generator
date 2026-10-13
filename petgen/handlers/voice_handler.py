"""Synthesize speech for the reply using the configured TTS backend."""

from __future__ import annotations

from petgen.models.config_model import AppConfig
from petgen.models.turn import Turn
from petgen.services.tts_backend import get_tts_backend


class VoiceHandler:
    name = "voice"

    async def handle(self, turn: Turn, config: AppConfig) -> Turn:
        if not turn.reply:
            return turn
        tts = get_tts_backend(config.services.tts)
        turn.audio_out = await tts.synthesize(
            text=turn.reply,
            voice=config.profile.voice_id,
            emotion=turn.emotion,
        )
        return turn