"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Memory Manager

Descrição: Gerenciador central de memórias.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.memory.profile import (
    ProfileMemory
)


class MemoryManager:

    def __init__(
        self,
        profile: ProfileMemory
    ):

        self.profile = profile

        self.repository = (
            profile.repository
        )

    def set(
        self,
        namespace: str,
        key: str,
        value: str
    ):

        self.repository.set(
            namespace,
            key,
            value
        )

    def get(
        self,
        namespace: str,
        key: str
    ):

        return self.repository.get(
            namespace,
            key
        )

    def delete(
        self,
        namespace: str,
        key: str
    ):

        query = """
        DELETE
        FROM nv_key_value
        WHERE namespace=%s
        AND item_key=%s
        """

        self.repository.db.execute_commit(
            query,
            (
                namespace,
                key
            )
        )

    def exists(
        self,
        namespace: str,
        key: str
    ) -> bool:

        return (
            self.get(
                namespace,
                key
            )
            is not None
        )
