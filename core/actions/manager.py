"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Manager

Descrição: Executor central de actions.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.registry import ActionRegistry
from core.actions.context import ActionContext


class ActionManager:

    def __init__(
        self,
        kernel=None
    ):

        self.kernel = kernel

        self.registry = ActionRegistry()

    async def execute(
        self,
        action_name: str,
        context=None,
        payload=None
    ):

        action = self.registry.get(
            action_name
        )

        if not action:

            raise ValueError(
                f"Action not found: {action_name}"
            )

        if context is None:

            context = ActionContext(
                kernel=self.kernel
            )

        return await action.execute(
            context=context,
            payload=payload
        )
