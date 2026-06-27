import asyncio

from pathlib import Path

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_hash.action import (
    FilesystemHashAction
)


async def main():

    arquivo = Path(
        "sandbox/hash_test.txt"
    )

    arquivo.write_text(
        "OMEGA DRAKON",
        encoding="utf-8"
    )

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemHashAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_hash",
            payload={
                "path":
                "sandbox/hash_test.txt"
            }
        )
    )

    print(
        result["success"]
    )

    print(
        result["algorithm"]
    )

    print(
        len(
            result["hash"]
        )
    )


asyncio.run(main())
