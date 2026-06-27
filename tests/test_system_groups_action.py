import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.system_groups.action import (
    SystemGroupsAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        SystemGroupsAction()
    )

    result = await (
        kernel.actions.execute(
            "system_groups"
        )
    )

    print(result)


asyncio.run(main())
