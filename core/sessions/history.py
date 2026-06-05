"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Session History

Descrição: Histórico persistente das conversas.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from llm.prompts.messages import (
    Message
)


class SessionHistory:

    def __init__(
        self,
        repository
    ):

        self.repository = repository

    def save(
        self,
        owner_id: str,
        source: str,
        role: str,
        content: str
    ):

        self.repository.save_message(
            owner_id,
            source,
            role,
            content
        )

    def load(
        self,
        owner_id: str,
        limit: int
    ):

        rows = self.repository.get_recent_messages(
            owner_id,
            limit
        )

        rows.reverse()

        return [

            Message(
                role=row["role"],
                content=row["content"]
            )

            for row in rows
        ]
