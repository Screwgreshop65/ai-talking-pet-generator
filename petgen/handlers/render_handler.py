"""Push the finished turn to the desktop window."""

from __future__ import annotations

import logging

from petgen.models.config_model import AppConfig
from petgen.models.turn import Turn

log = logging.getLogger(__name__)


class RenderHandler:
    name = "render"

    async def emit(self, turn: Turn, config: AppConfig) -> None:
        log.info(
            "render pet=%s intent=%s emotion=%s reply_len=%d",
            config.profile.name,
            turn.intent,
            turn.emotion,
            len(turn.reply or ""),
        )

    async def handle(self, turn: Turn, config: AppConfig) -> Turn:
        await self.emit(turn, config)
        return turn