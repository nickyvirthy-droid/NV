from core.events.event import Event
from core.events.types import EventType

from core.protocols.action_protocol import (
    ActionProtocol
)

from core.security.permissions import (
    PermissionManager
)

from core.security.errors import (
    ActionNotFoundError
)


class ActionExecutor:

    def __init__(
        self,
        registry,
        event_bus,
        logger,
        admin_mode: bool = False,
    ):

        self.registry = registry

        self.event_bus = event_bus

        self.logger = logger

        self.permissions = (
            PermissionManager(
                admin_mode=admin_mode
            )
        )

    async def execute(
        self,
        action_name,
        payload,
    ):

        definition = self.registry.get(
            action_name
        )

        if not definition:

            raise ActionNotFoundError(
                f"Action not found: "
                f"{action_name}"
            )

        self.permissions.validate(
            definition
        )

        protocol = ActionProtocol(
            action=action_name,
            payload=payload,
        )

        validated_payload = (
            definition.payload_model(
                **protocol.payload
            )
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

            result = definition.handler(
                validated_payload,
                payload.get("workspace"),
            )

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
