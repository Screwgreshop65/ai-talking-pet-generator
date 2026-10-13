"""Tiny async event bus for cross-stage signals."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

Handler = Callable[[Any], Awaitable[None]]


class EventBus:
    """Fan-out pub/sub. Subscribers run concurrently; errors are logged."""

    def __init__(self) -> None:
        self._subs: dict[str, list[Handler]] = {}

    def subscribe(self, topic: str, handler: Handler) -> None:
        self._subs.setdefault(topic, []).append(handler)

    async def publish(self, topic: str, payload: Any) -> None:
        handlers = self._subs.get(topic, [])
        if not handlers:
            return
        await asyncio.gather(*(h(payload) for h in handlers), return_exceptions=True)