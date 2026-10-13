# Contributing to ai-talking-pet-generator

Thanks for wanting to give a desk object a mouth. This repo is a modular
toolkit for generating AI-driven talking pets and talking objects on
Windows desktop. Read this before you open a PR.

## Ground rules

- Python 3.12 is the baseline. CI runs 3.12 and 3.13 on Windows and Linux.
- Every module under `petgen/` stays importable without a GPU. Heavy backends
  are lazy-loaded behind the `services/` layer.
- No new top-level dependency without a `pip-tools` compile in the same PR.
- Keep the pipeline stages decoupled: perception -> brain -> voice -> render.

## Layout

```
petgen/
  bootstrap/     entry points, CLI, app wiring
  core/          pipeline orchestration, event bus, registry
  handlers/      per-stage handlers (intent, emotion, animation)
  services/      external integrations (LLM, TTS, STT, avatar)
  models/        data models & schemas (pydantic)
  utils/         cross-cutting helpers
  config/        config loader + default profiles
```

If you add a new capability, decide which layer owns it before writing code.
If it touches a third-party API, it belongs in `services/`. If it transforms
data already in the pipeline, it belongs in `handlers/`.

## Adding a new pet profile

1. Drop a YAML file in `petgen/config/profiles/`.
2. Conform to the schema in `petgen/models/pet_profile.py`.
3. Add a smoke test to `tests/test_pet_profiles.py`.
4. Regenerate the profile index: `python -m petgen.utils.profile_index`.

## Adding a new voice backend

Implement `services.voice_backend.VoiceBackend` and register it in
`services/voice_registry.py`. Do not monkey-patch the default backend.

## Style

- `ruff format` + `ruff check` must pass.
- `mypy --strict` on `petgen/` (excluding `petgen/bootstrap/`).
- Docstrings on every public function. One-line is fine.
- Prefer dataclasses/pydantic over dict-of-dicts.

## Commit messages

`scope: short imperative summary` — e.g. `voice: add piper backend fallback`.

## Security

Do not commit API keys. See SECURITY.md for the disclosure process.