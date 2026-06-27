"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Search Action

Descrição: Busca arquivos e diretórios.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import BaseAction


class FilesystemSearchAction(BaseAction):

    name = "filesystem_search"

    description = (
        "Busca arquivos no filesystem."
    )

    async def execute(
        self,
        context,
        payload
    ):

        root = payload.get(
            "path",
            "."
        )

        pattern = payload.get(
            "pattern",
            "*"
        )

        results = []

        for item in Path(root).rglob(pattern):

            results.append(
                {
                    "name": item.name,
                    "path": str(item),
                    "type": (
                        "directory"
                        if item.is_dir()
                        else "file"
                    )
                }
            )

        return {
            "count": len(results),
            "items": results
        }
