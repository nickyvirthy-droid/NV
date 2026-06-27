import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_branch.action import (
    GitBranchAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        GitBranchAction()
    )

    result = await manager.execute(
        "git_branch"
    )

    print(result)


asyncio.run(main())
