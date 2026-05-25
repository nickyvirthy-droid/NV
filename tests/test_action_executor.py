import asyncio

from core.runtime.registry import (
    RuntimeRegistry
)

from core.actions.executor import (
    ActionExecutor
)


class DummyBus:

    async def emit(
        self,
        event,
    ):
        pass


class DummyLogger:

    def error(
        self,
        *args,
        **kwargs,
    ):
        print(
            "LOGGER ERROR:",
            args,
            kwargs,
        )


async def main():

    runtime = RuntimeRegistry()

    executor = ActionExecutor(
        registry=runtime.action_registry,
        event_bus=DummyBus(),
        logger=DummyLogger(),
    )

    result = await executor.execute(
        "filesystem.create_folder",
        {
            "path": "teste_runtime"
        }
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
