import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.database_query.action import (
    DatabaseQueryAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        DatabaseQueryAction()
    )

    result = await (
        kernel.actions.execute(
            "database_query",
            payload={
                "query":
                """
                SELECT *
                FROM nv_messages
                LIMIT 5
                """
            }
        )
    )

    print(result)


asyncio.run(main())
