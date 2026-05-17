import asyncio
from collections import defaultdict


class EventBus:
    def __init__(self):
        self.handlers = defaultdict(list)

    def subscribe(self, event_type, handler):
        self.handlers[event_type].append(handler)

    async def emit(self, event):
        handlers = self.handlers.get(event.type, [])

        await asyncio.gather(
            *(handler(event) for handler in handlers)
        )
