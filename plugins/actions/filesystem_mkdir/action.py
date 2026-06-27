"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Mkdir Action

Descrição: Cria diretórios.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import (
    BaseAction
)


class FilesystemMkdirAction(BaseAction):

    name = "filesystem_mkdir"

    description = (
        "Cria diretório."
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

        directory = Path(path)

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        return {
            "success": True,
            "path": str(directory)
        }
