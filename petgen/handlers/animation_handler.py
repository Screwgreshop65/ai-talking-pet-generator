"""Map emotion + viseme timing to an avatar animation clip."""

from __future__ import annotations

from petgen.models.config_model import AppConfig
from petgen.models.turn import Turn
from petgen.services.avatar_backend import get_avatar_backend


class AnimationHandler:
    name = "animation"

    async def handle(self, turn: Turn, config: AppConfig) -> Turn:
        if turn.audio_out is None:
            return turn
        avatar = get_avatar_backend(config.services.avatar)
        turn.animation = await avatar.plan_clip(
            audio=turn.audio_out,
            emotion=turn.emotion,
            rig=config.profile.rig_id,
        )
        return turn