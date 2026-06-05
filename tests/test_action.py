import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.system_info.action import (
    SystemInfoAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        SystemInfoAction()
    )

    result = await manager.execute(
        "system_info"
    )

    print(result)


asyncio.run(main())
