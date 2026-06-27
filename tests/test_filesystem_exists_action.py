import asyncio

from core.runtime.kernel import RuntimeKernel


async def main():

    kernel = RuntimeKernel()

    result = await kernel.actions.execute(
        "filesystem_exists",
        payload={
            "path": "docs/README.md"
        }
    )

    print(result)

    result = await kernel.actions.execute(
        "filesystem_exists",
        payload={
            "path": "arquivo_que_nao_existe.txt"
        }
    )

    print(result)


asyncio.run(main())
