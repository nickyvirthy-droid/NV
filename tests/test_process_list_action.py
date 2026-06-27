import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.process_list.action import (
    ProcessListAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        ProcessListAction()
    )

    result = await manager.execute(
        "process_list"
    )

    print(
        "processes:",
        result["count"]
    )

    print(
        result["processes"][:10]
    )


asyncio.run(main())
