import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_status.action import (
    GitStatusAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitStatusAction()
    )

    result = await (
        kernel.actions.execute(
            "git_status"
        )
    )

    print(result)


asyncio.run(main())
