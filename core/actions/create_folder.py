from pathlib import Path


async def create_folder(payload):
    path = payload["path"]

    folder = Path(path)
    folder.mkdir(parents=True, exist_ok=True)

    return {
        "success": True,
        "path": str(folder),
    }
