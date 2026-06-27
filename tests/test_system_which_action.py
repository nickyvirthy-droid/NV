import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.system_which.action import (
    SystemWhichAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        SystemWhichAction()
    )

    result = await (
        kernel.actions.execute(
            "system_which",
            payload={
                "command": "python3"
            }
        )
    )

    print(result)


asyncio.run(main())
