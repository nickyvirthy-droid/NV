import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.docker_list.action import (
    DockerListAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        DockerListAction()
    )

    result = await manager.execute(
        "docker_list"
    )

    print(result)


asyncio.run(main())
