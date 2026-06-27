import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.system_hostname.action import (
    SystemHostnameAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        SystemHostnameAction()
    )

    result = await (
        kernel.actions.execute(
            "system_hostname"
        )
    )

    print(result)


asyncio.run(main())
