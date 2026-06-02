"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Info Action

Descrição: Informações básicas do host.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import platform
import socket

from core.actions.base import BaseAction


class SystemInfoAction(BaseAction):

    name = "system_info"

    description = (
        "Retorna informações básicas "
        "do sistema."
    )

    async def execute(
        self,
        context,
        payload
    ):

        return {

            "runtime_started":
                context.kernel.state.started,

            "hostname":
                socket.gethostname(),

            "platform":
                platform.platform(),

            "python_version":
                platform.python_version(),
        }
