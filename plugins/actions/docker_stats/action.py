"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Docker Stats Action

Descrição: Retorna estatísticas de um container Docker.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import BaseAction


class DockerStatsAction(BaseAction):

    name = "docker_stats"

    description = (
        "Retorna estatísticas "
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
                "stats",
                container,
                "--no-stream",
                "--format",
                "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"
            ],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:

            raise ValueError(
                f"Container not found: {container}"
            )

        line = result.stdout.strip()

        (
            name,
            cpu_percent,
            memory_usage
        ) = line.split(
            "|",
            maxsplit=2
        )

        return {

            "name":
                name,

            "cpu_percent":
                cpu_percent,

            "memory_usage":
                memory_usage,
        }
