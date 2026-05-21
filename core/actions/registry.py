class ActionRegistry:
    def __init__(self):
        self.actions = {}

    def register(
        self,
        name,
        action,
        description="",
    ):
        self.actions[name] = {
            "handler": action,
            "description": description,
        }

    def get(
        self,
        name,
    ):
        return self.actions.get(name)

    def list_actions(self):
        return {
            name: data["description"]
            for name, data in self.actions.items()
        }
