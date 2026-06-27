import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.service_list.action import (
    ServiceListAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        ServiceListAction()
    )

    result = await manager.execute(
        "service_list"
    )

    print(
        "services:",
        result["count"]
    )

    print(
        result["services"][:10]
    )


asyncio.run(main())
