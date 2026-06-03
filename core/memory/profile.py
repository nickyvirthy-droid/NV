"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Profile Memory

Descrição: Memória persistente do perfil do usuário.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.database.repositories.key_value import (
    KeyValueRepository
)


class ProfileMemory:

    def __init__(
        self,
        repository: KeyValueRepository
    ):

        self.repository = repository

    def set_name(
        self,
        name: str
    ):

        self.repository.set(
            "profile",
            "user_name",
            name
        )

    def get_name(self):

        return self.repository.get(
            "profile",
            "user_name"
        )
