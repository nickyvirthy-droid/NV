from datetime import UTC
from datetime import datetime


class StateManager:
    def __init__(self):
        self.started_at = datetime.now(
            UTC,
        )

        self.runtime_status = "starting"

        self.capabilities = {}

        self.interfaces = []

        self.loaded_models = []

        self.actions = {}

    def set_runtime_status(
        self,
        status: str,
    ):
        self.runtime_status = status

    def register_capability(
        self,
        name: str,
        status: str = "online",
    ):
        self.capabilities[name] = {
            "status": status,
            "registered_at": datetime.now(
                UTC,
            ).isoformat(),
        }

    def get_state(self):
        uptime = (
            datetime.now(
                UTC,
            ) - self.started_at
        ).total_seconds()

        return {
            "runtime": {
                "status": self.runtime_status,
                "uptime_seconds": int(uptime),
            },
            "capabilities": self.capabilities,
            "interfaces": self.interfaces,
            "loaded_models": self.loaded_models,
            "actions": self.actions,
        }

    def set_actions(
        self,
        actions,
    ):
        self.actions = actions
