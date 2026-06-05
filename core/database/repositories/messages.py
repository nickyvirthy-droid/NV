"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Messages Repository

Descrição: Persistência do histórico de conversas.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.database.repositories.base import (
    BaseRepository
)


class MessagesRepository(
    BaseRepository
):

    def save_message(
        self,
        owner_id: str,
        source: str,
        role: str,
        content: str
    ):

        self.db.execute_commit(
            """
            INSERT INTO nv_messages
            (
                owner_id,
                source,
                role,
                content
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                owner_id,
                source,
                role,
                content
            )
        )

    def get_recent_messages(
        self,
        owner_id: str,
        limit: int
    ):

        return self.db.fetchall(
            """
            SELECT
                role,
                content
            FROM nv_messages
            WHERE owner_id=%s
            ORDER BY id DESC
            LIMIT %s
            """,
            (
                owner_id,
                limit
            )
        )
