import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_diff.action import (
    GitDiffAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitDiffAction()
    )

    result = await (
        kernel.actions.execute(
            "git_diff"
        )
    )

    print(result)


asyncio.run(main())
