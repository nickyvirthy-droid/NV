import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.ip_address.action import (
    IpAddressAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        IpAddressAction()
    )

    result = await manager.execute(
        "ip_address"
    )

    print(result)


asyncio.run(main())
