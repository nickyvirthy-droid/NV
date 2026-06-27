"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: CPU Info Action

Descrição: Retorna informações da CPU.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import psutil

from core.actions.base import BaseAction


class CpuInfoAction(BaseAction):

    name = "cpu_info"

    description = (
        "Retorna informações "
        "da CPU."
    )

    async def execute(
        self,
        context,
        payload
    ):

        return {

            "physical_cores":
                psutil.cpu_count(
                    logical=False
                ),

            "logical_cores":
                psutil.cpu_count(
                    logical=True
                ),

            "usage_percent":
                psutil.cpu_percent(
                    interval=1
                ),
        }
