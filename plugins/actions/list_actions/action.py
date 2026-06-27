"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: List Actions Action

Descrição: Lista actions registradas.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import BaseAction


class ListActionsAction(BaseAction):

    name = "list_actions"

    description = (
        "Lista actions "
        "registradas."
    )

    async def execute(
        self,
        context,
        payload
    ):

        return {

            "actions":
                context.kernel.actions
                .registry
                .list()
        }
