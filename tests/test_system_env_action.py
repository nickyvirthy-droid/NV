import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.system_env.action import (
    SystemEnvAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        SystemEnvAction()
    )

    result = await (
        kernel.actions.execute(
            "system_env",
            payload={
                "key": "HOME"
            }
        )
    )

    print(result)


asyncio.run(main())
