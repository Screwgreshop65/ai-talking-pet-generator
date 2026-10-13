"""Perception -> brain -> voice -> render pipeline for a single pet."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field

from petgen.core.registry import StageRegistry
from petgen.models.config_model import AppConfig
from petgen.models.pet_profile import PetProfile
from petgen.models.turn import Turn

log = logging.getLogger(__name__)


@dataclass(slots=True)
class PetPipeline:
    """Runs the turn loop for one pet. One instance per running pet."""

    config: AppConfig
    registry: StageRegistry
    _queue: asyncio.Queue[Turn] = field(default_factory=asyncio.Queue)
    _running: bool = False

    @property
    def profile(self) -> PetProfile:
        return self.config.profile

    async def start(self) -> None:
        self._running = True
        log.info("pipeline online for pet=%s", self.profile.name)
        await self._serve()

    async def stop(self) -> None:
        self._running = False
        await self._queue.put(Turn.sentinel())

    async def run(self, once: bool = False) -> None:
        await self.start()
        if once:
            await self.stop()

    async def _serve(self) -> None:
        while self._running:
            turn = await self._queue.get()
            if turn.is_sentinel:
                break
            await self._process(turn)

    async def _process(self, turn: Turn) -> None:
        stage_names = self.registry.order_for(self.profile.mode)
        for name in stage_names:
            stage = self.registry.get(name)
            turn = await stage.handle(turn, self.config)
            if turn.aborted:
                log.warning("turn aborted at stage=%s", name)
                break
        await self.registry.get("render").emit(turn, self.config)