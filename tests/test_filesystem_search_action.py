import asyncio

from core.runtime.kernel import RuntimeKernel


async def main():

    kernel = RuntimeKernel()

    result = await kernel.actions.execute(
        "filesystem_search",
        payload={
            "path": "plugins/actions",
            "pattern": "*.py"
        }
    )

    print(result["count"])

    print(
        result["items"][:10]
    )


asyncio.run(main())
