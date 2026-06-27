import asyncio

from core.security.approval_engine import (
    ApprovalEngine
)


async def main():

    engine = ApprovalEngine()

    result = await engine.validate(
        action_name="list_actions"
    )

    print(
        result.allowed
    )


asyncio.run(main())
