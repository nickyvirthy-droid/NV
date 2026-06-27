"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Disk Usage Action

Descrição: Informações de uso do disco.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import shutil

from core.actions.base import BaseAction


class DiskUsageAction(BaseAction):

    name = "disk_usage"

    description = (
        "Retorna informações "
        "de uso do disco."
    )

    async def execute(
        self,
        context,
        payload
    ):

        disk = shutil.disk_usage("/")

        return {

            "total_gb":
                round(
                    disk.total / 1024**3,
                    2
                ),

            "used_gb":
                round(
                    disk.used / 1024**3,
                    2
                ),

            "free_gb":
                round(
                    disk.free / 1024**3,
                    2
                ),

            "percent":
                round(
                    (
                        disk.used
                        / disk.total
                    ) * 100,
                    2
                ),
        }
