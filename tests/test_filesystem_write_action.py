import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)

from plugins.actions.filesystem_write.action import (
    FilesystemWriteAction
)


async def main():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        FilesystemWriteAction()
    )

    result = await (
        kernel.actions.execute(
            "filesystem_write",
            payload={
                "path":
                "sandbox/teste_write.txt",

                "content":
                "OMEGA DRAKON"
            }
        )
    )

    print(result)


asyncio.run(main())
