import asyncio

from core.runtime.kernel import RuntimeKernel


async def main():

    kernel = RuntimeKernel()

    result = await kernel.actions.execute(
        "list_actions"
    )

    print(type(result))
    print(result)


asyncio.run(main())
