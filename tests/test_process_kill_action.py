import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.process_kill.action import (
    ProcessKillAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        ProcessKillAction()
    )

    action = (
        kernel.actions.registry.get(
            "process_kill"
        )
    )

    print(
        action.name
    )

    print(
        action.dangerous
    )


asyncio.run(main())
