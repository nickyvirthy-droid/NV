"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Hostname Action

Descrição: Retorna hostname do sistema.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import socket

from core.actions.base import (
    BaseAction
)


class SystemHostnameAction(BaseAction):

    name = "system_hostname"

    description = (
        "Retorna hostname."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        return {
            "hostname":
            socket.gethostname()
        }
