from core.database.manager import (
    DatabaseManager
)

db = DatabaseManager()

result = db.fetchone(
    "SELECT VERSION() AS version"
)

print(result)
