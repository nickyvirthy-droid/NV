"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Memory Usage Action

Descrição: Retorna informações de uso
da memória do sistema.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import psutil

from core.actions.base import BaseAction


class MemoryUsageAction(BaseAction):

    name = "memory_usage"

    description = (
        "Retorna informações "
        "de uso da memória."
    )

    async def execute(
        self,
        context,
        payload
    ):

        memory = psutil.virtual_memory()

        return {

            "total_mb":
                round(
                    memory.total / 1024**2,
                    2
                ),

            "available_mb":
                round(
                    memory.available / 1024**2,
                    2
                ),

            "used_mb":
                round(
                    memory.used / 1024**2,
                    2
                ),

            "percent":
                memory.percent,
        }
