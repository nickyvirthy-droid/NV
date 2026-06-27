import asyncio

from core.security.scope_engine import (
    ScopeEngine
)


async def main():

    engine = ScopeEngine()

    result = await engine.validate(
        action_name="list_actions"
    )

    print(
        result.allowed
    )


asyncio.run(main())
