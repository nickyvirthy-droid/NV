"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Archive Action

Descrição: Compactação de arquivos e diretórios.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import shutil

from pathlib import Path

from core.actions.base import (
    BaseAction
)


class FilesystemArchiveAction(BaseAction):

    name = "filesystem_archive"

    description = (
        "Cria arquivo compactado."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        source = payload.get(
            "source"
        )

        output = payload.get(
            "output"
        )

        if not source:

            return {
                "success": False,
                "error": "source required"
            }

        if not output:

            return {
                "success": False,
                "error": "output required"
            }

        source_path = Path(source)

        if not source_path.exists():

            return {
                "success": False,
                "error": "source not found"
            }

        output_path = Path(output)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        archive_name = str(
            output_path.with_suffix("")
        )

        archive_format = (
            output_path.suffix
            .replace(".", "")
        )

        shutil.make_archive(
            archive_name,
            archive_format,
            root_dir=source
        )

        return {
            "success": True,
            "source": source,
            "output": output
        }
