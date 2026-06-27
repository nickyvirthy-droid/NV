from core.sessions.manager import (
    SessionManager
)

manager = SessionManager()

session = manager.create()

print(session.id)

loaded = manager.get(
    session.id
)

print(
    loaded.id == session.id
)
