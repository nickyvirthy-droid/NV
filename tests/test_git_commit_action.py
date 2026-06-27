import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_commit.action import (
    GitCommitAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitCommitAction()
    )

    result = await (
        kernel.actions.execute(
            "git_commit",
            payload={
                "message":
                "teste runtime"
            }
        )
    )

    print(result)


asyncio.run(main())
