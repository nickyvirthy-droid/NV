"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Validate Action

Descrição: Valida existência e disponibilidade de uma action.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)


class ActionValidateAction(BaseAction):

    name = "action_validate"

    description = (
        "Valida uma action."
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
                "valid": False,
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
                "valid": False,
                "error": "action not found"
            }

        return {
            "success": True,
            "valid": True,
            "action": action.name,
            "description": action.description,
            "dangerous": getattr(
                action,
                "dangerous",
                False
            )
        }
