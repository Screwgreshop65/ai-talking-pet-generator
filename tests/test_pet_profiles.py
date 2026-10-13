"""Validate every shipped pet profile against the schema."""

from __future__ import annotations

import pytest
import yaml

from petgen.models.pet_profile import PetProfile
from petgen.utils.paths import config_dir


def _profile_paths() -> list:
    return sorted((config_dir() / "profiles").glob("*.yaml"))


@pytest.mark.parametrize("path", _profile_paths(), ids=lambda p: p.stem)
def test_profile_validates(path) -> None:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    profile = PetProfile.model_validate(raw)
    assert profile.name
    assert profile.persona.name
    assert profile.mode in {"companion", "chat", "prop"}
</thinking>