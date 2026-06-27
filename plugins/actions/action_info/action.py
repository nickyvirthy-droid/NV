"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Info Action

Descrição: Retorna informações de uma action.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)


class ActionInfoAction(BaseAction):

    name = "action_info"

    description = (
        "Retorna informações de uma action."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        action_name = payload.get(
            "action"
        )

        if not action_name:

            return {
                "success": False,
                "error": "action required"
            }

        action = (
            context.kernel
            .actions
            .registry
            .get(action_name)
        )

        if not action:

            return {
                "success": False,
                "error": "action not found"
            }

        return {
            "success": True,
            "name": action.name,
            "description": action.description,
            "dangerous": getattr(
                action,
                "dangerous",
                False
            )
        }
