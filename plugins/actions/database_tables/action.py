"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Database Tables Action

Descrição: Lista tabelas MariaDB.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.database.manager import (
    DatabaseManager
)


class DatabaseTablesAction(BaseAction):

    name = "database_tables"

    description = (
        "Lista tabelas do banco."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        db = DatabaseManager()

        rows = db.fetchall(
            "SHOW TABLES"
        )

        tables = [
            list(row.values())[0]
            for row in rows
        ]

        return {
            "tables": tables
        }
