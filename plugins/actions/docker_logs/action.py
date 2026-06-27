"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Docker Logs Action

Descrição: Retorna logs de um container Docker.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import BaseAction


class DockerLogsAction(BaseAction):

    name = "docker_logs"

    description = (
        "Retorna logs "
        "de um container Docker."
    )

    async def execute(
        self,
        context,
        payload
    ):

        payload = payload or {}

        container = payload.get(
            "container"
        )

        if not container:

            raise ValueError(
                "container is required"
            )

        tail = payload.get(
            "tail",
            50
        )

        result = subprocess.run(
            [
                "docker",
                "logs",
                container,
                "--tail",
                str(tail)
            ],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:

            raise ValueError(
                f"Container not found: {container}"
            )

        output = (
            result.stdout
            if result.stdout
            else result.stderr
        )

        lines = output.splitlines()


        return {

            "container":
                container,

            "count":
                len(lines),

            "logs":
                lines,
        }
