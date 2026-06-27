import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.list_actions.action import (
    ListActionsAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        ListActionsAction()
    )

    result = await manager.execute(
        "list_actions"
    )

    print(result)


asyncio.run(main())
