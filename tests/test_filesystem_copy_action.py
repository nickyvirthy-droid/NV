import asyncio

from pathlib import Path

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_copy.action import (
    FilesystemCopyAction
)


async def main():

    Path(
        "sandbox/origem_copy.txt"
    ).write_text(
        "OMEGA"
    )

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemCopyAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_copy",
            payload={
                "source":
                "sandbox/origem_copy.txt",

                "destination":
                "sandbox/destino_copy.txt"
            }
        )
    )

    print(result)

    print(
        Path(
            "sandbox/origem_copy.txt"
        ).exists()
    )

    print(
        Path(
            "sandbox/destino_copy.txt"
        ).exists()
    )

    print(
        Path(
            "sandbox/destino_copy.txt"
        ).read_text()
    )


asyncio.run(main())
