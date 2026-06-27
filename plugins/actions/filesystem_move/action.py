"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Move Action

Descrição: Move arquivos e diretórios.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path
import shutil

from core.actions.base import (
    BaseAction
)


class FilesystemMoveAction(BaseAction):

    name = "filesystem_move"

    description = (
        "Move arquivos."
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

        shutil.move(
            source,
            destination
        )

        return {
            "success": True,
            "source": source,
            "destination": destination
        }
