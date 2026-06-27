"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Docker List Action

Descrição: Lista containers Docker.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import BaseAction


class DockerListAction(BaseAction):

    name = "docker_list"

    description = (
        "Lista containers Docker."
    )

    async def execute(
        self,
        context,
        payload
    ):

        result = subprocess.run(
            [
                "docker",
                "ps",
                "--format",
                "{{.ID}}|{{.Names}}|{{.Image}}|{{.Status}}"
            ],
            capture_output=True,
            text=True,
            check=False
        )

        containers = []

        for line in result.stdout.splitlines():

            if not line.strip():
                continue

            container_id, name, image, status = (
                line.split(
                    "|",
                    maxsplit=3
                )
            )

            containers.append(
                {
                    "id": container_id,
                    "name": name,
                    "image": image,
                    "status": status,
                }
            )

        return {

            "count":
                len(containers),

            "containers":
                containers,
        }
