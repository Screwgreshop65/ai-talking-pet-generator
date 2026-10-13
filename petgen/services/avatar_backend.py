"""Avatar/animation planner. 2D rig planner ships in-tree."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from petgen.models.config_model import AvatarServiceConfig
from petgen.services.tts_backend import AudioClip


@dataclass(frozen=True, slots=True)
class AnimationClip:
    rig: str
    fps: int
    visemes: tuple[int, ...]


class AvatarBackend(Protocol):
    async def plan_clip(self, *, audio: AudioClip, emotion: str, rig: str) -> AnimationClip: ...


class Rig2DPlanner:
    """Naive viseme spread based on clip duration. Good enough for a desk pet."""

    async def plan_clip(self, *, audio: AudioClip, emotion: str, rig: str) -> AnimationClip:
        duration_ms = int(len(audio.pcm) / 2 / audio.sample_rate * 1000)
        frames = max(1, duration_ms // 40)
        visemes = tuple((i % 8) for i in range(frames))
        return AnimationClip(rig=rig, fps=25, visemes=visemes)


def get_avatar_backend(config: AvatarServiceConfig) -> AvatarBackend:
    return Rig2DPlanner()