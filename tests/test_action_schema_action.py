import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.action_schema.action import (
    ActionSchemaAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        ActionSchemaAction()
    )

    result = await (
        kernel.actions.execute(
            "action_schema",
            payload={
                "action":
                "filesystem_read"
            }
        )
    )

    print(
        result["success"]
    )

    print(
        result["action"]
    )

    print(
        isinstance(
            result["schema"],
            dict
        )
    )


asyncio.run(main())
