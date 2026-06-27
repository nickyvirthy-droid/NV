"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Write Action

Descrição: Escreve conteúdo em arquivo.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import (
    BaseAction
)


class FilesystemWriteAction(BaseAction):

    name = "filesystem_write"

    description = (
        "Escreve conteúdo em arquivo."
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

        content = payload.get(
            "content",
            ""
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

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "success": True,
            "path": str(file_path)
        }
