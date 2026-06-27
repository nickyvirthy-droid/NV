"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Read Action

Descrição: Lê conteúdo de arquivos.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import BaseAction


class FilesystemReadAction(BaseAction):

    name = "filesystem_read"

    description = (
        "Lê um arquivo do filesystem."
    )

    async def execute(
        self,
        context,
        payload
    ):

        file_path = payload.get(
            "path"
        )

        if not file_path:

            raise ValueError(
                "path is required"
            )

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                file_path
            )

        if not path.is_file():

            raise ValueError(
                "path is not a file"
            )

        content = path.read_text(
            encoding="utf-8"
        )

        return {
            "path": str(path),
            "size": len(content),
            "content": content
        }
