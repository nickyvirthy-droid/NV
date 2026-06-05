from core.database.manager import (
    DatabaseManager
)

from core.database.repositories.messages import (
    MessagesRepository
)

from core.sessions.history import (
    SessionHistory
)

db = DatabaseManager()

repo = MessagesRepository(
    db
)

history = SessionHistory(
    repo
)

history.save(
    "alex",
    "cli",
    "user",
    "Olá Nicky"
)

messages = history.load(
    "alex",
    10
)

for message in messages:

    print(
        message.role,
        message.content
    )
