"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Ping Action

Descrição: Testa conectividade de rede.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import (
    BaseAction
)


class SystemPingAction(BaseAction):

    name = "system_ping"

    description = (
        "Executa ping em host."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        host = payload.get(
            "host",
            "8.8.8.8"
        )

        result = subprocess.run(
            [
                "ping",
                "-c",
                "1",
                host
            ],
            capture_output=True,
            text=True
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "host": host,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
