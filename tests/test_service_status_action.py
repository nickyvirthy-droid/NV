import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.service_status.action import (
    ServiceStatusAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        ServiceStatusAction()
    )

    result = await manager.execute(
        "service_status",
        payload={
            "service":
                "nicky.service"
        }
    )

    print(result)


asyncio.run(main())
