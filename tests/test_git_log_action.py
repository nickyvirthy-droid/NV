import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_log.action import (
    GitLogAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitLogAction()
    )

    result = await (
        kernel.actions.execute(
            "git_log"
        )
    )

    print(result)


asyncio.run(main())
