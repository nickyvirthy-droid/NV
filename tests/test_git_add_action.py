import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_add.action import (
    GitAddAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitAddAction()
    )

    result = await (
        kernel.actions.execute(
            "git_add",
            payload={
                "files": [
                    "core/coder.py"
                ]
            }
        )
    )

    print(result)


asyncio.run(main())
