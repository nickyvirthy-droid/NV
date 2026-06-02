"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Session Manager

Descrição: Gerenciamento de sessões do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.sessions.session import Session


class SessionManager:

    def __init__(self):

        self.sessions: dict[str, Session] = {}

    def create(self) -> Session:

        session = Session()

        self.sessions[session.id] = session

        return session

    def get(self, session_id: str):

        return self.sessions.get(session_id)

    def append_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        session = self.get(session_id)

        if not session:
            return

        session.messages.append({
            "role": role,
            "content": content
        })
