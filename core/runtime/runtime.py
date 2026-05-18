from core.runtime.registry import RuntimeRegistry
from core.state.manager import StateManager

from observability.logging.logger import setup_logger


class NickyRuntime:
    def __init__(self):
        self.registry = RuntimeRegistry()

        self.logger = setup_logger()

        self.state_manager = StateManager()

    async def startup(self):
        self.logger.info(
            "runtime_starting",
        )

        self.registry.register(
            "logger",
            self.logger,
        )

        self.registry.register(
            "state_manager",
            self.state_manager,
        )

        self.logger.info(
            "runtime_started",
        )

    async def shutdown(self):
        self.logger.info(
            "runtime_shutdown",
        )
