"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Service Logs Action

Descrição: Retorna logs de um serviço.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import BaseAction


class ServiceLogsAction(BaseAction):

    name = "service_logs"

    description = (
        "Retorna logs "
        "de um serviço."
    )

    async def execute(
        self,
        context,
        payload
    ):

        payload = payload or {}

        service = payload.get(
            "service"
        )

        if not service:

            raise ValueError(
                "service is required"
            )

        tail = payload.get(
            "tail",
            50
        )

        result = subprocess.run(
            [
                "journalctl",
                "-u",
                service,
                "-n",
                str(tail),
                "--no-pager",
            ],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:

            raise ValueError(
                f"Service not found: {service}"
            )

        lines = result.stdout.splitlines()

        return {

            "service":
                service,

            "count":
                len(lines),

            "logs":
                lines,
        }
