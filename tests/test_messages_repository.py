from core.database.manager import (
    DatabaseManager
)

from core.database.repositories.messages import (
    MessagesRepository
)

db = DatabaseManager()

repo = MessagesRepository(
    db
)

repo.save_message(
    owner_id="teste",
    source="cli",
    role="user",
    content="Olá NV"
)

messages = repo.get_recent_messages(
    "teste",
    10
)

print(
    len(messages)
)

print(
    messages[0]
)
