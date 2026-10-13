"""App-wide configuration models."""

from __future__ import annotations

from pydantic import BaseModel, Field

from petgen.models.pet_profile import PetProfile


class LLMServiceConfig(BaseModel):
    backend: str = "echo"
    base_url: str | None = None
    api_key_env: str = "PETGEN_LLM_KEY"
    model_path: str | None = None
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.7


class TTSServiceConfig(BaseModel):
    backend: str = "silent"
    model_path: str | None = None
    voice_dir: str = "voice_cache"


class STTServiceConfig(BaseModel):
    backend: str = "passthrough"
    model_path: str | None = None


class AvatarServiceConfig(BaseModel):
    backend: str = "rig2d"
    rigs_dir: str = "petgen/config/rigs"


class ServicesConfig(BaseModel):
    llm: LLMServiceConfig = Field(default_factory=LLMServiceConfig)
    tts: TTSServiceConfig = Field(default_factory=TTSServiceConfig)
    stt: STTServiceConfig = Field(default_factory=STTServiceConfig)
    avatar: AvatarServiceConfig = Field(default_factory=AvatarServiceConfig)


class AppConfig(BaseModel):
    profile: PetProfile
    services: ServicesConfig = Field(default_factory=ServicesConfig)
    log_level: str = "INFO"