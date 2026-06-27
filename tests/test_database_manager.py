from core.database.manager import (
    DatabaseManager
)

db = DatabaseManager()

print(
    db.fetchone(
        "SELECT VERSION() AS version"
    )
)
