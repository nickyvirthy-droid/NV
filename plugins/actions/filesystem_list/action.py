"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem List Action

Descrição: Lista arquivos e diretórios.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import BaseAction


class FilesystemListAction(BaseAction):

    name = "filesystem_list"

    description = (
        "Lista conteúdo de um diretório."
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

        path = Path(root)

        if not path.exists():

            raise FileNotFoundError(
                root
            )

        if not path.is_dir():

            raise ValueError(
                "path is not a directory"
            )

        items = []

        for item in sorted(
            path.iterdir()
        ):

            items.append(
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
            "count": len(items),
            "items": items
        }
