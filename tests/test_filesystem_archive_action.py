import asyncio

from pathlib import Path

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_archive.action import (
    FilesystemArchiveAction
)


async def main():

    pasta = Path(
        "sandbox/archive_test"
    )

    pasta.mkdir(
        parents=True,
        exist_ok=True
    )

    (
        pasta / "teste.txt"
    ).write_text(
        "OMEGA DRAKON",
        encoding="utf-8"
    )

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemArchiveAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_archive",
            payload={
                "source":
                "sandbox/archive_test",

                "output":
                "sandbox/archive_test.zip"
            }
        )
    )

    print(
        result["success"]
    )

    print(
        Path(
            "sandbox/archive_test.zip"
        ).exists()
    )


asyncio.run(main())
