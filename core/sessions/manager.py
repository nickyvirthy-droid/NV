from core.sessions.session import (
    RuntimeSession
)


class SessionManager:

    def __init__(self):

        self.sessions = {}

    def create(
        self,
        user_id="default",
    ):

        session = RuntimeSession(
            user_id=user_id
        )

        self.sessions[
            session.session_id
        ] = session

        return session

    def get(
        self,
        session_id,
    ):

        return self.sessions.get(
            session_id
        )

    def add_memory(
        self,
        session_id,
        message,
    ):

        session = self.get(
            session_id
        )

        if not session:
            return

        session.memory.append(
            message
        )
