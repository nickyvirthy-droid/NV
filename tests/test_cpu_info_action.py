import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.cpu_info.action import (
    CpuInfoAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        CpuInfoAction()
    )

    result = await manager.execute(
        "cpu_info"
    )

    print(result)


asyncio.run(main())
