import asyncio

from core.actions.manager import ActionManager

from plugins.actions.system_info.action import (
    SystemInfoAction
)


async def main():

    manager = ActionManager()

    manager.registry.register(
        SystemInfoAction()
    )

    result = await manager.execute(
        "system_info"
    )

    print(result)


asyncio.run(main())
