"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Extract Action

Descrição: Extrai arquivos compactados.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import shutil

from pathlib import Path

from core.actions.base import (
    BaseAction
)


class FilesystemExtractAction(BaseAction):

    name = "filesystem_extract"

    description = (
        "Extrai arquivos compactados."
    )

    dangerous = True

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        archive = payload.get(
            "archive"
        )

        destination = payload.get(
            "destination"
        )

        if not archive:

            return {
                "success": False,
                "error": "archive required"
            }

        if not destination:

            return {
                "success": False,
                "error": "destination required"
            }

        archive_path = Path(
            archive
        )

        if not archive_path.exists():

            return {
                "success": False,
                "error": "archive not found"
            }

        Path(
            destination
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.unpack_archive(
            archive,
            destination
        )

        return {
            "success": True,
            "archive": archive,
            "destination": destination
        }
