"""A Turn is one user -> pet -> user cycle."""

from __future__ import annotations

from dataclasses import dataclass, field

from petgen.services.avatar_backend import AnimationClip
from petgen.services.tts_backend import AudioClip


@dataclass(slots=True)
class Turn:
    text: str | None = None
    audio: bytes | None = None
    intent: str = "unknown"
    emotion: str = "neutral"
    reply: str | None = None
    audio_out: AudioClip | None = None
    animation: AnimationClip | None = None
    aborted: bool = False
    meta: dict[str, str] = field(default_factory=dict)

    @property
    def is_sentinel(self) -> bool:
        return self.meta.get("__sentinel__") == "1"

    @classmethod
    def sentinel(cls) -> "Turn":
        return cls(meta={"__sentinel__": "1"})