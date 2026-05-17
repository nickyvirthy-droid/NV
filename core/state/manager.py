class StateManager:
    def __init__(self):
        self.state = {
            "active_users": [],
            "loaded_models": [],
            "interfaces": [],
            "health": "healthy",
        }

    def get_state(self):
        return self.state
