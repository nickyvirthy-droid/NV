from core.runtime.registry import RuntimeRegistry
from core.state.manager import StateManager

from core.events.bus import EventBus

from observability.logging.logger import setup_logger

from core.events.handlers.system import log_all_events
from core.events.types import EventType

class NickyRuntime:
    def __init__(self):
        self.registry = RuntimeRegistry()

        self.logger = setup_logger()

        self.state_manager = StateManager()

        self.event_bus = EventBus(
            logger=self.logger,
        )

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

        self.state_manager.set_runtime_status(
            "running",
        )

        self.state_manager.register_capability(
            "event_bus",
        )

        self.state_manager.register_capability(
            "state_manager",
        )

        self.state_manager.register_capability(
            "logger",
        )

        self.logger.info(
            "runtime_started",
        )
        self.registry.register(
            "event_bus",
            self.event_bus,
        )
        for event_type in EventType:
            self.event_bus.subscribe(
                event_type,
                log_all_events,
        )

    async def shutdown(self):
        self.logger.info(
            "runtime_shutdown",
        )
