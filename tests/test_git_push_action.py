import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_push.action import (
    GitPushAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitPushAction()
    )

    result = await (
        kernel.actions.execute(
            "git_push"
        )
    )

    print(result)


asyncio.run(main())
