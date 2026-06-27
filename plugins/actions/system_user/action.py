"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System User Action

Descrição: Retorna usuário atual.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import getpass

from core.actions.base import (
    BaseAction
)


class SystemUserAction(BaseAction):

    name = "system_user"

    description = (
        "Retorna usuário atual."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        return {
            "user": getpass.getuser()
        }
