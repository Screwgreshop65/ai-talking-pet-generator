"""Stage registry — maps stage names to handler instances."""

from __future__ import annotations

from collections.abc import Iterable

from petgen.handlers.animation_handler import AnimationHandler
from petgen.handlers.emotion_handler import EmotionHandler
from petgen.handlers.intent_handler import IntentHandler
from petgen.handlers.perception_handler import PerceptionHandler
from petgen.handlers.render_handler import RenderHandler
from petgen.handlers.voice_handler import VoiceHandler


class StageRegistry:
    """Ordered map of stage name -> handler. Order is per-mode."""

    def __init__(self, stages: dict[str, object]) -> None:
        self._stages = stages

    @classmethod
    def default(cls) -> "StageRegistry":
        return cls(
            {
                "perception": PerceptionHandler(),
                "intent": IntentHandler(),
                "emotion": EmotionHandler(),
                "voice": VoiceHandler(),
                "animation": AnimationHandler(),
                "render": RenderHandler(),
            }
        )

    def get(self, name: str) -> object:
        return self._stages[name]

    def order_for(self, mode: str) -> Iterable[str]:
        common = ["perception", "intent", "emotion"]
        tail = ["voice", "animation", "render"]
        if mode == "chat":
            return common + ["voice", "render"]
        return common + tail