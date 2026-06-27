"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Info Action

Descrição: Informações detalhadas de arquivos e diretórios.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path
from datetime import datetime

from core.actions.base import BaseAction


class FilesystemInfoAction(BaseAction):

    name = "filesystem_info"

    description = (
        "Retorna informações de um caminho."
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

        if not path.exists():

            raise FileNotFoundError(
                target
            )

        stat = path.stat()

        return {
            "path": str(path),
            "name": path.name,
            "exists": True,
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).isoformat()
        }
