import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.memory_usage.action import (
    MemoryUsageAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        MemoryUsageAction()
    )

    result = await manager.execute(
        "memory_usage"
    )

    print(result)


asyncio.run(main())
