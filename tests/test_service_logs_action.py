import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.service_logs.action import (
    ServiceLogsAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        ServiceLogsAction()
    )

    result = await manager.execute(
        "service_logs",
        payload={
            "service":
                "nicky.service",
            "tail":
                5,
        }
    )

    print(result)


asyncio.run(main())
