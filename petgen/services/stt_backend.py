"""STT backend selection: whisper.cpp bridge if present, else passthrough."""

from __future__ import annotations

from typing import Protocol

from petgen.models.config_model import STTServiceConfig


class STTBackend(Protocol):
    async def transcribe(self, audio: bytes) -> str: ...


class PassthroughSTT:
    """Returns empty text — perception handler will abort the turn."""

    async def transcribe(self, audio: bytes) -> str:
        return ""


def get_stt_backend(config: STTServiceConfig) -> STTBackend:
    if config.backend == "whisper_cpp" and config.model_path:
        from petgen.services.stt_whisper import WhisperCppBackend

        return WhisperCppBackend(config)
    return PassthroughSTT()