import asyncio
import sqlite3

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.database_tables.action import (
    DatabaseTablesAction
)


async def main():

    db = "sandbox/test.db"

    conn = sqlite3.connect(db)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER
        )
        """
    )

    conn.commit()
    conn.close()

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        DatabaseTablesAction()
    )

    result = await (
        kernel.actions.execute(
            "database_tables",
            payload={
                "database": db
            }
        )
    )

    print(result)


asyncio.run(main())
