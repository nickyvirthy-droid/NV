from pathlib import Path

from core.security.filesystem import (
    is_path_allowed,
)


async def create_folder(payload):
    path = payload["path"]

    if not is_path_allowed(path):
        raise PermissionError(
            "Path not allowed"
        )

    folder = Path(path)

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    return {
        "success": True,
        "path": str(folder),
    }
