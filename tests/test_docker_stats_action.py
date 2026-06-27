import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.docker_stats.action import (
    DockerStatsAction
)


async def main():

    kernel = RuntimeKernel()

    manager = kernel.actions

    manager.registry.register(
        DockerStatsAction()
    )

    result = await manager.execute(
        "docker_stats",
        payload={
            "container": "mariadb"
        }
    )

    print(result)


asyncio.run(main())
