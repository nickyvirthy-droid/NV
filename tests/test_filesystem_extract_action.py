import asyncio

from pathlib import Path

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_extract.action import (
    FilesystemExtractAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemExtractAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_extract",
            payload={
                "archive":
                "sandbox/archive_test.zip",

                "destination":
                "sandbox/extracted"
            }
        )
    )

    print(
        result["success"]
    )

    print(
        Path(
            "sandbox/extracted/teste.txt"
        ).exists()
    )


asyncio.run(main())
