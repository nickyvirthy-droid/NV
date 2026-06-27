import asyncio

from core.runtime.kernel import RuntimeKernel


async def main():

    kernel = RuntimeKernel()

    result = await kernel.actions.execute(
        "filesystem_read",
        payload={
            "path": "docs/README.md"
        }
    )

    print(
        result["path"]
    )

    print(
        result["size"]
    )

    print(
        result["content"][:500]
    )


asyncio.run(main())
