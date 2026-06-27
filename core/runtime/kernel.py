"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Runtime Kernel

Descrição: Núcleo principal do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.events.bus import EventBus
from core.registry.services import ServiceContainer
from core.state.runtime_state import RuntimeState
from plugins.loader import PluginLoader
from config.runtime import RuntimeConfig
from llm.providers.manager import ProviderManager
from llm.providers.llamacpp import LlamaCppProvider
from core.sessions.manager import SessionManager
from core.actions.manager import ActionManager
from plugins.actions.loader import (
    register_actions
)
from core.database.manager import (
    DatabaseManager
)
from core.database.repositories.key_value import (
    KeyValueRepository
)
from core.memory.profile import (
    ProfileMemory
)
from core.memory.manager import (
    MemoryManager
)
from core.database.repositories.messages import (
    MessagesRepository
)
from core.database.repositories.workflow_executions import (
    WorkflowExecutionsRepository
)
from core.sessions.history import (
    SessionHistory
)
from core.coder import (
    CoderEngine
)
from core.workflows.manager import (
    WorkflowManager
)
from plugins.workflows.loader import (
    register_workflows
)

class RuntimeKernel:

    def __init__(self):

        self.config = RuntimeConfig()

        self.container = ServiceContainer()

        self.events = EventBus()

        self.state = RuntimeState()

        self.plugins = PluginLoader(
            plugin_dir=self.config.plugins_dir
        )

        self.providers = ProviderManager()

        self.sessions = SessionManager()

        self.actions = ActionManager(
            kernel=self
        )

        self.database = DatabaseManager()

        messages_repo = MessagesRepository(
            self.database
        )

        workflow_repo = (
            WorkflowExecutionsRepository(
                self.database
            )
        )

        self.history = SessionHistory(
            messages_repo
        )

        repo = KeyValueRepository(
            self.database
        )

        profile = ProfileMemory(
            repo
        )

        self.memory = MemoryManager(
            profile
        )

        self.coder = CoderEngine()

        self.workflows = WorkflowManager(
            kernel=self
        )

        self.workflow_repo = (
            workflow_repo
        )

        register_actions(
            self.actions
        )

        register_workflows(
            self.workflows
        )

        self._register_core_services()

    async def boot(self):

        self.state.started = True

        discovered = self.plugins.discover()

        await self.load_providers()

        await self.events.emit(
            "SYSTEM_BOOT",
            {
                "status": "initializing",
                "plugins": discovered
            }
        )

    async def shutdown(self):

        self.state.started = False

        await self.events.emit(
            "SYSTEM_SHUTDOWN",
            {"status": "stopping"}
        )

    def _register_core_services(self):

        self.container.register(
            "config",
            self.config
        )

        self.container.register(
            "events",
            self.events
        )

        self.container.register(
            "state",
            self.state
        )

        self.container.register(
            "plugins",
            self.plugins
        )

        self.container.register(
            "providers",
            self.providers
        )

        self.container.register(
            "sessions",
            self.sessions
        )

        self.container.register(
            "actions",
            self.actions
        )

        self.container.register(
            "database",
            self.database
        )

        self.container.register(
            "memory",
            self.memory
        )

        self.container.register(
            "coder",
            self.coder
        )

        self.container.register(
            "history",
            self.history
        )

        self.container.register(
            "workflows",
            self.workflows
        )

        self.container.register(
            "workflow_repo",
            self.workflow_repo
        )

    async def load_providers(self):

        llamacpp = LlamaCppProvider()

        self.providers.register(llamacpp)
