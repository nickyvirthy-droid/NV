"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Uptime Action

Descrição: Tempo de atividade do sistema.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import time

from core.actions.base import BaseAction


class UptimeAction(BaseAction):

    name = "uptime"

    description = (
        "Retorna tempo ativo."
    )

    async def execute(
        self,
        context,
        payload
    ):

        uptime = time.time() - time.monotonic()

        return {
            "seconds": int(uptime)
        }
