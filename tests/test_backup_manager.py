from pathlib import Path

from core.coder import (
    BackupManager
)

Path(
    "teste_backup.txt"
).write_text(
    "NV"
)

backup = BackupManager()

backup_file = (
    backup.create_backup(
        "teste_backup.txt"
    )
)

print(
    Path(
        backup_file
    ).exists()
)

Path(
    "teste_backup.txt"
).unlink()
