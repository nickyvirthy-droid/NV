"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Which Action

Descrição: Localiza executáveis no sistema.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import shutil

from core.actions.base import (
    BaseAction
)


class SystemWhichAction(BaseAction):

    name = "system_which"

    description = (
        "Localiza executáveis."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        command = payload.get(
            "command"
        )

        if not command:

            return {
                "found": False
            }

        path = shutil.which(
            command
        )

        return {
            "found": path is not None,
            "path": path
        }
