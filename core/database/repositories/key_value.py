"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Key Value Repository

Descrição: Persistência genérica do NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.database.repositories.base import (
    BaseRepository
)


class KeyValueRepository(
    BaseRepository
):

    def set(
        self,
        namespace,
        key,
        value
    ):

        self.db.execute_commit(
            """
            INSERT INTO nv_key_value
            (
                namespace,
                item_key,
                item_value
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            ON DUPLICATE KEY UPDATE
                item_value = VALUES(item_value)
            """,
            (
                namespace,
                key,
                value
            )
        )

    def get(
        self,
        namespace,
        key
    ):

        result = self.db.fetchone(
            """
            SELECT item_value
            FROM nv_key_value
            WHERE namespace=%s
            AND item_key=%s
            """,
            (
                namespace,
                key
            )
        )

        if not result:
            return None

        return result["item_value"]
