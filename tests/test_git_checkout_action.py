import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.git_checkout.action import (
    GitCheckoutAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        GitCheckoutAction()
    )

    result = await (
        kernel.actions.execute(
            "git_checkout",
            payload={
                "branch": "develop"
            }
        )
    )

    print(result)


asyncio.run(main())
