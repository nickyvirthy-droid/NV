"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Copy Action

Descrição: Copia arquivos.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path
import shutil

from core.actions.base import (
    BaseAction
)


class FilesystemCopyAction(BaseAction):

    name = "filesystem_copy"

    description = (
        "Copia arquivos."
    )

    dangerous = True

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        source = payload.get(
            "source"
        )

        destination = payload.get(
            "destination"
        )

        if not source or not destination:

            return {
                "success": False,
                "error": (
                    "source and destination required"
                )
            }

        if not Path(source).exists():

            return {
                "success": False,
                "error": "source not found"
            }

        shutil.copy2(
            source,
            destination
        )

        return {
            "success": True,
            "source": source,
            "destination": destination
        }
