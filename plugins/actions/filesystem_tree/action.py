"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Tree Action

Descrição: Retorna árvore de diretórios.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path

from core.actions.base import (
    BaseAction
)


class FilesystemTreeAction(BaseAction):

    name = "filesystem_tree"

    description = (
        "Retorna árvore de diretórios."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        root = Path(
            payload.get(
                "path",
                "."
            )
        )

        max_depth = int(
            payload.get(
                "depth",
                3
            )
        )

        if not root.exists():

            return {
                "success": False,
                "error": "path not found"
            }

        items = []

        def walk(
            current,
            depth=0
        ):

            if depth > max_depth:
                return

            try:

                for child in sorted(
                    current.iterdir()
                ):

                    items.append(
                        {
                            "name": child.name,
                            "path": str(child),
                            "is_dir": child.is_dir(),
                            "depth": depth
                        }
                    )

                    if child.is_dir():

                        walk(
                            child,
                            depth + 1
                        )

            except Exception:
                pass

        walk(root)

        return {
            "success": True,
            "root": str(root),
            "count": len(items),
            "items": items
        }
