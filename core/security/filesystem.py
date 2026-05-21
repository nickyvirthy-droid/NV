from pathlib import Path


ALLOWED_PATHS = [
    Path("/home/alex/NV"),
]


def is_path_allowed(
    path: str,
) -> bool:
    try:
        resolved = Path(path).resolve()

        for allowed in ALLOWED_PATHS:
            if resolved.is_relative_to(
                allowed.resolve()
            ):
                return True

        return False

    except Exception:
        return False
