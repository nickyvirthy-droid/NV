class ActionExecutor:
    def __init__(self, registry):
        self.registry = registry

    async def execute(self, action_name, payload):
        action = self.registry.get(action_name)

        if not action:
            raise ValueError("Action not found")

        return await action(payload)
