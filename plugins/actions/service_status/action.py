"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Service Status Action

Descrição: Retorna status detalhado de um serviço.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import BaseAction


class ServiceStatusAction(BaseAction):

    name = "service_status"

    description = (
        "Retorna status "
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

        result = subprocess.run(
            [
                "systemctl",
                "show",
                service,
                "--property=Id",
                "--property=ActiveState",
                "--property=SubState",
                "--property=MainPID",
                "--property=ExecMainStartTimestamp",
            ],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:

            raise ValueError(
                f"Service not found: {service}"
            )

        data = {}

        for line in result.stdout.splitlines():

            if "=" not in line:
                continue

            key, value = line.split(
                "=",
                maxsplit=1
            )

            data[key] = value

        return {

            "id":
                data.get("Id"),

            "active_state":
                data.get("ActiveState"),

            "sub_state":
                data.get("SubState"),

            "main_pid":
                int(
                    data.get(
                        "MainPID",
                        "0"
                    )
                ),

            "started_at":
                data.get(
                    "ExecMainStartTimestamp"
                ),
        }
