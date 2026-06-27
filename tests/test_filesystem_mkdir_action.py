import asyncio

from pathlib import Path

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_mkdir.action import (
    FilesystemMkdirAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemMkdirAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_mkdir",
            payload={
                "path":
                "sandbox/test_dir/subdir"
            }
        )
    )

    print(result)

    print(
        Path(
            "sandbox/test_dir/subdir"
        ).exists()
    )


asyncio.run(main())
