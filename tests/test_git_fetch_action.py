import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_fetch.action import (
    GitFetchAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitFetchAction()
    )

    result = await (
        kernel.actions.execute(
            "git_fetch"
        )
    )

    print(result)


asyncio.run(main())
