"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Schema Action

Descrição: Retorna schema de uma action.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import inspect

from core.actions.base import (
    BaseAction
)


class ActionSchemaAction(BaseAction):

    name = "action_schema"

    description = (
        "Retorna schema de uma action."
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

        schema = getattr(
            action,
            "schema",
            {}
        )

        if not schema:

            signature = inspect.signature(
                action.execute
            )

            schema = {
                str(name): str(param.annotation)
                for name, param
                in signature.parameters.items()
                if name not in (
                    "self",
                    "context",
                    "payload"
                )
            }

        return {
            "success": True,
            "action": action_name,
            "schema": schema
        }
