"""Smoke tests for the turn pipeline using offline backends."""

from __future__ import annotations

import pytest

from petgen.core.pipeline import PetPipeline
from petgen.core.registry import StageRegistry
from petgen.models.config_model import AppConfig
from petgen.models.pet_profile import Persona, PetProfile
from petgen.models.turn import Turn


def _config() -> AppConfig:
    profile = PetProfile(
        name="Testy",
        mode="companion",
        persona=Persona(name="Testy", species="test", catchphrase="beep."),
    )
    return AppConfig(profile=profile)


@pytest.mark.asyncio
async def test_pipeline_processes_a_turn() -> None:
    pipeline = PetPipeline(config=_config(), registry=StageRegistry.default())
    turn = Turn(text="hello there")
    await pipeline._process(turn)
    assert turn.intent == "greet"
    assert turn.reply is not None
    assert turn.audio_out is not None
    assert turn.animation is not None
    assert not turn.aborted


@pytest.mark.asyncio
async def test_empty_text_aborts() -> None:
    pipeline = PetPipeline(config=_config(), registry=StageRegistry.default())
    turn = Turn(text="   ")
    await pipeline._process(turn)
    assert turn.aborted