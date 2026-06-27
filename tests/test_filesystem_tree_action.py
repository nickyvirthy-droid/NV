import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_tree.action import (
    FilesystemTreeAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemTreeAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_tree",
            payload={
                "path": "plugins",
                "depth": 1
            }
        )
    )

    print(
        result["success"]
    )

    print(
        result["count"] > 0
    )

    print(
        result["items"][0]["name"]
    )


asyncio.run(main())
