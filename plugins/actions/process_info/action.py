"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Process Info Action

Descrição: Retorna detalhes de um processo.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import psutil

from core.actions.base import BaseAction


class ProcessInfoAction(BaseAction):

    name = "process_info"

    description = (
        "Retorna detalhes "
        "de um processo."
    )

    async def execute(
        self,
        context,
        payload
    ):

        payload = payload or {}

        pid = payload.get(
            "pid"
        )

        if pid is None:

            raise ValueError(
                "pid is required"
            )

        process = psutil.Process(
            pid
        )

        memory = (
            process.memory_info().rss
            / 1024**2
        )

        return {

            "pid":
                process.pid,

            "name":
                process.name(),

            "status":
                process.status(),

            "cpu_percent":
                process.cpu_percent(),

            "memory_mb":
                round(
                    memory,
                    2
                ),

            "threads":
                process.num_threads(),
        }
