import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.action_info.action import (
    ActionInfoAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        ActionInfoAction()
    )

    result = await (
        kernel.actions.execute(
            "action_info",
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
        result["name"]
    )

    print(
        "description" in result
    )


asyncio.run(main())
