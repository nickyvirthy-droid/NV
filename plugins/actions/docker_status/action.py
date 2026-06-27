"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Docker Status Action

Descrição: Retorna detalhes de um container Docker.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import BaseAction


class DockerStatusAction(BaseAction):

    name = "docker_status"

    description = (
        "Retorna detalhes "
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

        result = subprocess.run(
            [
                "docker",
                "inspect",
                container,
                "--format",
                "{{.Id}}|{{.State.Status}}|{{.State.StartedAt}}|{{.RestartCount}}"
            ],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:

            raise ValueError(
                f"Container not found: {container}"
            )

        (
            container_id,
            status,
            started_at,
            restart_count
        ) = result.stdout.strip().split(
            "|",
            maxsplit=3
        )

        return {

            "id":
                container_id,

            "name":
                container,

            "status":
                status,

            "started_at":
                started_at,

            "restart_count":
                int(restart_count),
        }
