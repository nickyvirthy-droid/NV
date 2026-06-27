import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.system_exec.action import (
    SystemExecAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        SystemExecAction()
    )

    result = await (
        kernel.actions.execute(
            "system_exec",
            payload={
                "command": "pwd"
            }
        )
    )

    print(result)


asyncio.run(main())
