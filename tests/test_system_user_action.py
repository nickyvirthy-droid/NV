import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.system_user.action import (
    SystemUserAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        SystemUserAction()
    )

    result = await (
        kernel.actions.execute(
            "system_user"
        )
    )

    print(result)


asyncio.run(main())
