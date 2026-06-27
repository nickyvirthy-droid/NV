"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Process List Action

Descrição: Lista processos ativos.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import psutil

from core.actions.base import BaseAction


class ProcessListAction(BaseAction):

    name = "process_list"

    description = (
        "Lista processos "
        "ativos."
    )

    async def execute(
        self,
        context,
        payload
    ):

        processes = []

        for proc in psutil.process_iter(
            [
                "pid",
                "name",
                "status"
            ]
        ):

            try:

                processes.append(
                    proc.info
                )

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):

                continue

        return {

            "count":
                len(processes),

            "processes":
                processes,
        }
