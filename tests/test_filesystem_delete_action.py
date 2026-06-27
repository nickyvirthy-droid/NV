import asyncio

from pathlib import Path

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_delete.action import (
    FilesystemDeleteAction
)


async def main():

    Path(
        "sandbox/delete_me.txt"
    ).write_text(
        "teste"
    )

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemDeleteAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_delete",
            payload={
                "path":
                "sandbox/delete_me.txt"
            }
        )
    )

    print(result)

    print(
        Path(
            "sandbox/delete_me.txt"
        ).exists()
    )


asyncio.run(main())
