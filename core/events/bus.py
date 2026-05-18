import asyncio
from collections import defaultdict
from collections.abc import Callable

from core.events.event import Event


class EventBus:
    def __init__(self, logger=None):
        self.handlers = defaultdict(list)
        self.logger = logger

    def subscribe(
        self,
        event_type,
        handler: Callable,
    ):
        self.handlers[event_type].append(handler)

        if self.logger:
            self.logger.info(
                "event_handler_registered",
                event_type=event_type.value,
                handler=handler.__name__,
            )

    def unsubscribe(
        self,
        event_type,
        handler: Callable,
    ):
        if handler in self.handlers[event_type]:
            self.handlers[event_type].remove(handler)

    async def emit(
        self,
        event: Event,
    ):
        handlers = self.handlers.get(
            event.type,
            [],
        )

        if self.logger:
            self.logger.info(
                "event_emitted",
                event_type=event.type.value,
                source=event.source,
                event_id=event.id,
            )

        results = await asyncio.gather(
            *(handler(event) for handler in handlers),
            return_exceptions=True,
        )

        for result in results:
            if isinstance(result, Exception):
                if self.logger:
                    self.logger.error(
                        "event_handler_failed",
                        error=str(result),
                        event_type=str(event.type),
                    )
