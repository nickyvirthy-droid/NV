import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.docker_logs.action import (
    DockerLogsAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        DockerLogsAction()
    )

    result = await manager.execute(
        "docker_logs",
        payload={
            "container": "mariadb",
            "tail": 5
        }
    )

    print(result)


asyncio.run(main())
