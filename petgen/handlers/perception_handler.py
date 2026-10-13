"""Turn text/audio into a normalized perception payload."""

from __future__ import annotations

from petgen.models.config_model import AppConfig
from petgen.models.turn import Turn
from petgen.services.stt_backend import get_stt_backend


class PerceptionHandler:
    name = "perception"

    async def handle(self, turn: Turn, config: AppConfig) -> Turn:
        if turn.audio is not None:
            stt = get_stt_backend(config.services.stt)
            turn.text = await stt.transcribe(turn.audio)
        turn.text = (turn.text or "").strip()
        if not turn.text:
            turn.aborted = True
        return turn