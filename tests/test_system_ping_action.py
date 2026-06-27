import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.system_ping.action import (
    SystemPingAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        SystemPingAction()
    )

    result = await (
        kernel.actions.execute(
            "system_ping",
            payload={
                "host": "8.8.8.8"
            }
        )
    )

    print(result)


asyncio.run(main())
