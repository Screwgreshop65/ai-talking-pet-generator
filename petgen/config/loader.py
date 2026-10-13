"""Load the app config: defaults -> profile YAML -> optional override."""

from __future__ import annotations

from pathlib import Path

import yaml

from petgen.models.config_model import AppConfig
from petgen.models.pet_profile import PetProfile
from petgen.utils.paths import config_dir


def _load_profile(name: str) -> PetProfile:
    profile_path = config_dir() / "profiles" / f"{name}.yaml"
    if not profile_path.exists():
        raise FileNotFoundError(f"pet profile not found: {profile_path}")
    raw = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    return PetProfile.model_validate(raw)


def load_config(profile: str = "default_cat", override_path: str | None = None) -> AppConfig:
    """Resolve the full config. Override YAML is deep-merged last."""
    base = AppConfig(profile=_load_profile(profile))
    if override_path:
        override_path_obj = Path(override_path)
        if not override_path_obj.exists():
            raise FileNotFoundError(f"override config not found: {override_path_obj}")
        override_raw = yaml.safe_load(override_path_obj.read_text(encoding="utf-8")) or {}
        merged = base.model_dump()
        _deep_merge(merged, override_raw)
        return AppConfig.model_validate(merged)
    return base


def _deep_merge(target: dict, source: dict) -> None:
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_merge(target[key], value)
        else:
            target[key] = value