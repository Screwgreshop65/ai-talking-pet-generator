"""Repo-relative path helpers so tools work from any cwd."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def config_dir() -> Path:
    return REPO_ROOT / "petgen" / "config"


def outputs_dir() -> Path:
    path = REPO_ROOT / "outputs"
    path.mkdir(parents=True, exist_ok=True)
    return path