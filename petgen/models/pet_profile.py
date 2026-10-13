"""Pet profile schema — the YAML that defines one talking pet."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class Persona(BaseModel):
    """Voice + tone knobs fed into the LLM prompt."""

    name: str
    species: str = "unknown"
    tone: str = "friendly"
    catchphrase: str = ""
    backstory: str = ""
    taboos: list[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def _name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("persona.name must not be blank")
        return value.strip()


class PetProfile(BaseModel):
    """Full profile for a single pet or talking object."""

    name: str
    mode: str = "companion"  # companion | chat | prop
    rig_id: str = "rig2d_default"
    voice_id: str = "en_US-amy-low"
    persona: Persona
    tags: list[str] = Field(default_factory=list)

    @field_validator("mode")
    @classmethod
    def _valid_mode(cls, value: str) -> str:
        allowed = {"companion", "chat", "prop"}
        if value not in allowed:
            raise ValueError(f"mode must be one of {sorted(allowed)}")
        return value