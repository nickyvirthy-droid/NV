"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Database Query Action

Descrição: Executa consulta SQL no MariaDB.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.database.manager import (
    DatabaseManager
)


class DatabaseQueryAction(BaseAction):

    name = "database_query"

    description = (
        "Executa consulta SQL."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        query = payload.get(
            "query"
        )

        db = DatabaseManager()

        rows = db.fetchall(
            query
        )

        return {
            "rows": rows
        }
