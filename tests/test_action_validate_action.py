import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.action_validate.action import (
    ActionValidateAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        ActionValidateAction()
    )

    result = await (
        kernel.actions.execute(
            "action_validate",
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
        result["valid"]
    )

    print(
        result["action"]
    )


asyncio.run(main())
