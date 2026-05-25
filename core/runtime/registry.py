from core.registry.action_registry import ActionRegistry
from core.registry.discovery import load_actions


class RuntimeRegistry:

    def __init__(self):

        self._services: dict[str, object] = {}

        self.action_registry = ActionRegistry()

        load_actions(self.action_registry)

    def register(
        self,
        name: str,
        service: object
    ):

        self._services[name] = service

    def get(self, name: str):

        return self._services.get(name)

    def all(self):

        return self._services
