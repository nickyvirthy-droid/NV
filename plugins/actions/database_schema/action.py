"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Database Schema Action

Descrição: Retorna schema MariaDB.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.database.manager import (
    DatabaseManager
)


class DatabaseSchemaAction(BaseAction):

    name = "database_schema"

    description = (
        "Retorna schema da tabela."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        table = payload.get(
            "table"
        )

        db = DatabaseManager()

        schema = db.fetchall(
            f"DESCRIBE {table}"
        )

        return {
            "table": table,
            "schema": schema
        }
