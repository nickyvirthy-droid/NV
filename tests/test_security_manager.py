import asyncio

from core.security.manager import (
    SecurityManager
)


async def main():

    security = SecurityManager()

    result = await security.validate(
        action_name="list_actions"
    )

    print(
        result.allowed
    )


asyncio.run(main())
