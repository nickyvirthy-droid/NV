class ActionRegistry:
    def __init__(self):
        self.actions = {}

    def register(
        self,
        name,
        action,
        description="",
        safe=True,
    ):
        self.actions[name] = {
            "handler": action,
            "description": description,
            "safe": safe,
            "type": "action",
        }

    def get(
        self,
        name,
    ):
        return self.actions.get(name)

    def list_actions(self):
        return {
            name: {
                "description": data[
                    "description"
                ],
                "safe": data[
                    "safe"
                ],
                "type": data[
                    "type"
                ],
            }
            for name, data in self.actions.items()
        }
