import asyncio

from core.runtime.kernel import RuntimeKernel


async def main():

    kernel = RuntimeKernel()

    result = await kernel.actions.execute(
        "filesystem_list",
        payload={
            "path": "docs"
        }
    )

    print(
        result["count"]
    )

    print(
        result["items"][:20]
    )


asyncio.run(main())
