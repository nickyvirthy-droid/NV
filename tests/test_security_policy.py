import asyncio

from core.security.policy_engine import (
    PolicyEngine
)


async def main():

    engine = PolicyEngine()

    result = await engine.validate(
        action_name="list_actions"
    )

    print(
        result.allowed
    )


asyncio.run(main())
