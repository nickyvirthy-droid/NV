import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)


async def main():

    kernel = RuntimeKernel()

    result = await kernel.actions.execute(
        "disk_usage"
    )

    print(result)


asyncio.run(main())
