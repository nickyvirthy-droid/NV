"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Registry

Descrição: Registro central de actions.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import BaseAction


class ActionRegistry:

    def __init__(self):

        self._actions: dict[str, BaseAction] = {}

    def register(
        self,
        action: BaseAction
    ):

        self._actions[action.name] = action

    def get(
        self,
        name: str
    ):

        return self._actions.get(name)

    def list(self):

        return list(self._actions.keys())
