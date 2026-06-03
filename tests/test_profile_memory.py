from core.database.manager import (
    DatabaseManager
)

from core.database.repositories.key_value import (
    KeyValueRepository
)

from core.memory.profile import (
    ProfileMemory
)

db = DatabaseManager()

repo = KeyValueRepository(
    db
)

memory = ProfileMemory(
    repo
)

memory.set_name(
    "Alex"
)

print(
    memory.get_name()
)
