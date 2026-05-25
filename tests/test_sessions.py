from core.sessions.manager import (
    SessionManager
)


manager = SessionManager()

session = manager.create(
    user_id="alex"
)

manager.add_memory(
    session.session_id,
    {
        "role": "user",
        "content": "hello"
    }
)

loaded = manager.get(
    session.session_id
)

print(
    loaded.session_id
)

print(
    loaded.user_id
)

print(
    loaded.memory
)
