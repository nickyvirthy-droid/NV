"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Service List Action

Descrição: Lista serviços ativos.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import BaseAction


class ServiceListAction(BaseAction):

    name = "service_list"

    description = (
        "Lista serviços "
        "ativos."
    )

    async def execute(
        self,
        context,
        payload
    ):

        result = subprocess.run(
            [
                "systemctl",
                "list-units",
                "--type=service",
                "--state=running",
                "--no-pager",
                "--no-legend",
            ],
            capture_output=True,
            text=True,
            check=False
        )

        services = []

        for line in result.stdout.splitlines():

            if not line.strip():
                continue

            parts = line.split()

            services.append(
                {
                    "unit": parts[0],
                    "active": parts[2],
                    "sub": parts[3],
                }
            )

        return {

            "count":
                len(services),

            "services":
                services,
        }
