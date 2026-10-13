"""TTS backend selection: piper if available, else a silent stub."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from petgen.models.config_model import TTSServiceConfig


@dataclass(frozen=True, slots=True)
class AudioClip:
    pcm: bytes
    sample_rate: int


class TTSBackend(Protocol):
    async def synthesize(self, *, text: str, voice: str, emotion: str) -> AudioClip: ...


class SilentTTS:
    """Emits a zeroed PCM buffer sized to the text length. Used in tests/CI."""

    async def synthesize(self, *, text: str, voice: str, emotion: str) -> AudioClip:
        samples = max(1, len(text)) * 160
        return AudioClip(pcm=b"\x00" * samples * 2, sample_rate=22050)


def get_tts_backend(config: TTSServiceConfig) -> TTSBackend:
    if config.backend == "piper" and config.model_path:
        from petgen.services.tts_piper import PiperBackend

        return PiperBackend(config)
    return SilentTTS()