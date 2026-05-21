from core.runtime.registry import RuntimeRegistry
from core.state.manager import StateManager

from core.events.bus import EventBus

from observability.logging.logger import setup_logger

from core.events.handlers.system import log_all_events
from core.events.types import EventType

from core.actions.create_folder import create_folder
from core.actions.executor import ActionExecutor
from core.actions.registry import ActionRegistry

from llm.chat.service import ChatService
from llm.providers.llamacpp import (
    LlamaCppProvider,
)

class NickyRuntime:
    def __init__(self):
        self.registry = RuntimeRegistry()

        self.logger = setup_logger()

        self.state_manager = StateManager()

        self.event_bus = EventBus(
            logger=self.logger,
        )

        self.action_registry = ActionRegistry()

        self.action_executor = ActionExecutor(
            registry=self.action_registry,
            event_bus=self.event_bus,
            logger=self.logger,
        )

        self.llm_provider = LlamaCppProvider(
            base_url="http://127.0.0.1:8081",
        )

        self.chat_service = ChatService(
            provider=self.llm_provider,
        )

        self.loaded_models = []

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

        self.state_manager.register_capability(
            "action_executor",
        )

        for event_type in EventType:
            self.event_bus.subscribe(
                event_type,
                log_all_events,
        )

        self.action_registry.register(
            "filesystem.create_folder",
            create_folder,
            description="Create folder inside workspace sandbox",
        )

        self.state_manager.set_actions(
            self.action_registry.list_actions()
        )

        self.loaded_models.append(
            "Qwen2.5-3B-Instruct"
        )

        self.state_manager.loaded_models = (
            self.loaded_models
        )

        self.state_manager.register_capability(
            "llm_provider",
        )

    async def shutdown(self):
        self.logger.info(
            "runtime_shutdown",
        )
