from dataclasses import dataclass
from typing import Callable
from typing import Type


@dataclass
class ActionDefinition:

    name: str
    description: str

    safe: bool = True

    dangerous: bool = False

    admin_only: bool = False

    requires_confirmation: bool = False

    category: str = "general"

    version: str = "1.0"

    payload_model: Type = None

    handler: Callable = None


class ActionRegistry:

    def __init__(self):

        self._actions = {}

    def register(
        self,
        definition: ActionDefinition
    ):

        self._actions[
            definition.name
        ] = definition

    def get(
        self,
        name: str
    ):

        return self._actions.get(
            name
        )

    def list_actions(self):

        return list(
            self._actions.values()
        )
