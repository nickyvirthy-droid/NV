import asyncio

from core.security.audit_engine import (
    AuditEngine
)


async def main():

    engine = AuditEngine()

    result = await engine.record(
        action_name="list_actions",
        allowed=True
    )

    print(
        result.allowed
    )


asyncio.run(main())
