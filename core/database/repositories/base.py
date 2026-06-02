"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Base Repository

Descrição: Repositório base para acesso ao banco.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.database.manager import DatabaseManager


class BaseRepository:

    def __init__(
        self,
        db: DatabaseManager
    ):
        self.db = db
