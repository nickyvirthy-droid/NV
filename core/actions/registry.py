class ActionRegistry:
    def __init__(self):
        self.actions = {}

    def register(self, name, action):
        self.actions[name] = action

    def get(self, name):
        return self.actions.get(name)
