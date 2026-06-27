import asyncio

from pathlib import Path

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_move.action import (
    FilesystemMoveAction
)


async def main():

    Path(
        "sandbox/origem.txt"
    ).write_text(
        "NV"
    )

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemMoveAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_move",
            payload={
                "source":
                "sandbox/origem.txt",

                "destination":
                "sandbox/destino.txt"
            }
        )
    )

    print(result)

    print(
        Path(
            "sandbox/origem.txt"
        ).exists()
    )

    print(
        Path(
            "sandbox/destino.txt"
        ).exists()
    )


asyncio.run(main())
