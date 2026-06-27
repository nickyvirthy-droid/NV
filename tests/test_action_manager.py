import asyncio

from core.runtime.kernel import (
    RuntimeKernel
)


async def main():

    kernel = RuntimeKernel()

    result = await (
        kernel.actions.execute(
            "list_actions"
        )
    )

    print(
        isinstance(
            result,
            dict
        )
    )

    print(
        "actions" in result
    )

    print(
        len(
            result["actions"]
        )
    )

asyncio.run(main())
