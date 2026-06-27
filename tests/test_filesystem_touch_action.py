import asyncio

from pathlib import Path

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_touch.action import (
    FilesystemTouchAction
)


async def main():

    arquivo = Path(
        "sandbox/touch_test.txt"
    )

    if arquivo.exists():

        arquivo.unlink()

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemTouchAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_touch",
            payload={
                "path":
                "sandbox/touch_test.txt"
            }
        )
    )

    print(result)

    print(
        arquivo.exists()
    )

    print(
        arquivo.stat().st_size
    )


asyncio.run(main())
