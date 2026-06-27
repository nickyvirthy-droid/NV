from core.sessions.session import (
    Session
)

session = Session()

print(
    isinstance(
        session.id,
        str
    )
)

print(
    len(session.messages)
)

print(
    len(session.metadata)
)
