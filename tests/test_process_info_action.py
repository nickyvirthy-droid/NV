import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.process_info.action import (
    ProcessInfoAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        ProcessInfoAction()
    )

    result = await manager.execute(
        "process_info",
        payload={
            "pid": 1
        }
    )

    print(result)


asyncio.run(main())
