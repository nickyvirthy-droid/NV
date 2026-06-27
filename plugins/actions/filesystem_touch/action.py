"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Touch Action

Descrição: Cria arquivo vazio.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import (
    BaseAction
)


class FilesystemTouchAction(BaseAction):

    name = "filesystem_touch"

    description = (
        "Cria arquivo vazio."
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

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.touch(
            exist_ok=True
        )

        return {
            "success": True,
            "path": path
        }
