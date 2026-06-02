from core.database.manager import (
    DatabaseManager
)

from core.database.repositories.key_value import (
    KeyValueRepository
)

db = DatabaseManager()

repo = KeyValueRepository(
    db
)

repo.set(
    "memory",
    "user_name",
    "Alex"
)

value = repo.get(
    "memory",
    "user_name"
)

print(value)
