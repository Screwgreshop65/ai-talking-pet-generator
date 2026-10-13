"""Desktop app bootstrap: wires the pipeline and starts the UI loop."""

from __future__ import annotations

import logging

from petgen.config.loader import load_config
from petgen.core.pipeline import PetPipeline
from petgen.core.registry import StageRegistry
from petgen.utils.logging_setup import configure_logging

log = logging.getLogger(__name__)


class PetApp:
    """Thin wrapper that owns the pipeline lifecycle for the desktop shell."""

    def __init__(self, profile: str = "default_cat") -> None:
        configure_logging()
        self.config = load_config(profile=profile)
        self.pipeline = PetPipeline(config=self.config, registry=StageRegistry.default())

    async def start(self) -> None:
        log.info("pet app starting with profile=%s", self.config.profile.name)
        await self.pipeline.start()

    async def stop(self) -> None:
        await self.pipeline.stop()
        log.info("pet app stopped")