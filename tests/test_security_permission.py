import asyncio

from core.security.permission_engine import (
    PermissionEngine
)


async def main():

    engine = PermissionEngine()

    result = await engine.validate(
        action_name="list_actions"
    )

    print(
        result.allowed
    )


asyncio.run(main())
