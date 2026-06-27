from pathlib import Path

from core.coder import (
    BackupManager,
    RollbackManager
)

Path(
    "teste_restore.txt"
).write_text(
    "original"
)

backup = BackupManager()

backup_file = (
    backup.create_backup(
        "teste_restore.txt"
    )
)

Path(
    "teste_restore.txt"
).write_text(
    "alterado"
)

rollback = (
    RollbackManager()
)

rollback.restore(
    backup_file,
    "teste_restore.txt"
)

print(
    Path(
        "teste_restore.txt"
    ).read_text()
)

Path(
    "teste_restore.txt"
).unlink()
