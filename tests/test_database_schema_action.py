import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.database_schema.action import (
    DatabaseSchemaAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        DatabaseSchemaAction()
    )

    result = await (
        kernel.actions.execute(
            "database_schema",
            payload={
                "table": "nv_messages"
            }
        )
    )

    print(result)


asyncio.run(main())
