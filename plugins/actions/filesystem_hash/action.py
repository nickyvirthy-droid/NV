"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Filesystem Hash Action

Descrição: Gera hash de arquivos.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import hashlib

from pathlib import Path

from core.actions.base import (
    BaseAction
)


class FilesystemHashAction(BaseAction):

    name = "filesystem_hash"

    description = (
        "Calcula hash de arquivo."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        path = payload.get(
            "path"
        )

        algorithm = payload.get(
            "algorithm",
            "sha256"
        )

        if not path:

            return {
                "success": False,
                "error": "path required"
            }

        file_path = Path(path)

        if not file_path.exists():

            return {
                "success": False,
                "error": "file not found"
            }

        hasher = hashlib.new(
            algorithm
        )

        with open(
            file_path,
            "rb"
        ) as f:

            while chunk := f.read(
                8192
            ):
                hasher.update(
                    chunk
                )

        return {
            "success": True,
            "path": path,
            "algorithm": algorithm,
            "hash": hasher.hexdigest()
        }
