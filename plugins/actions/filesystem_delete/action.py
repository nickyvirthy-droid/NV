"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Delete Action

Descrição: Remove arquivo do sistema.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import (
    BaseAction
)


class FilesystemDeleteAction(BaseAction):

    name = "filesystem_delete"

    description = (
        "Remove arquivo."
    )

    dangerous = True

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        path = payload.get(
            "path"
        )

        if not path:

            return {
                "success": False,
                "error": "path required"
            }

        file_path = Path(path)

        if not file_path.exists():

            return {
                "success": False,
                "error": "file not found"
            }

        file_path.unlink()

        return {
            "success": True,
            "path": str(file_path)
        }
