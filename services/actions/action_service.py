from core.protocols.action_protocol import ActionProtocol


class ActionService:

    def __init__(self, registry):
        self.registry = registry

    def execute(
        self,
        data: dict,
        workspace
    ):

        protocol = ActionProtocol(**data)

        definition = self.registry.get(
            protocol.action
        )

        if not definition:
            raise ValueError(
                f"Unknown action: {protocol.action}"
            )

        payload = definition.payload_model(
            **protocol.payload
        )

        return definition.handler(
            payload,
            workspace
        )
