from pathlib import Path

from config.settings import settings


class PathResolver:
    @staticmethod
    def resolve(path):
        path = path.strip()

        if path.startswith("/"):
            return path

        return str(
            Path(
                settings.WORKSPACE_ROOT
            ) / path
        )
