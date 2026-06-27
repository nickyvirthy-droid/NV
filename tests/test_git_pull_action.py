import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_pull.action import (
    GitPullAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitPullAction()
    )

    result = await (
        kernel.actions.execute(
            "git_pull"
        )
    )

    print(result)


asyncio.run(main())
