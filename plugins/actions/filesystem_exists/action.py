"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Exists Action

Descrição: Verifica existência de arquivo ou diretório.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import BaseAction


class FilesystemExistsAction(BaseAction):

    name = "filesystem_exists"

    description = (
        "Verifica se um caminho existe."
    )

    async def execute(
        self,
        context,
        payload
    ):

        target = payload.get(
            "path"
        )

        if not target:

            raise ValueError(
                "path is required"
            )

        path = Path(target)

        return {
            "path": str(path),
            "exists": path.exists(),
            "is_file": path.is_file(),
            "is_directory": path.is_dir()
        }
