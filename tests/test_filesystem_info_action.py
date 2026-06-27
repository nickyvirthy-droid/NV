import asyncio

from core.runtime.kernel import RuntimeKernel


async def main():

    kernel = RuntimeKernel()

    result = await kernel.actions.execute(
        "filesystem_info",
        payload={
            "path": "docs/README.md"
        }
    )

    print(result)


asyncio.run(main())
