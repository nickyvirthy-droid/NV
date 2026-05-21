from core.events.event import Event
from core.events.types import EventType


class ActionExecutor:
    def __init__(
        self,
        registry,
        event_bus,
        logger,
    ):
        self.registry = registry
        self.event_bus = event_bus
        self.logger = logger

    async def execute(
        self,
        action_name,
        payload,
    ):
        action_data = self.registry.get(
            action_name,
        )

        if not action_data:
            raise ValueError(
                "Action not found"
            )

        await self.event_bus.emit(
            Event(
                type=EventType.ACTION_REQUESTED,
                source="action_executor",
                payload={
                    "action": action_name,
                },
            )
        )

        try:
            result = await action_data[
                "handler"
            ](payload)

            await self.event_bus.emit(
                Event(
                    type=EventType.ACTION_COMPLETED,
                    source="action_executor",
                    payload={
                        "action": action_name,
                        "success": True,
                    },
                )
            )

            return {
                "success": True,
                "action": action_name,
                "result": result,
            }

        except Exception as error:
            self.logger.error(
                "action_failed",
                action=action_name,
                error=str(error),
            )

            return {
                "success": False,
                "error": str(error),
            }
