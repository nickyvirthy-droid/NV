import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.docker_status.action import (
    DockerStatusAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        DockerStatusAction()
    )

    result = await manager.execute(
        "docker_status",
        payload={
            "container": "mariadb"
        }
    )

    print(result)


asyncio.run(main())
