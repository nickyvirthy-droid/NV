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

    async def load_providers(self):

        llamacpp = LlamaCppProvider()

        self.providers.register(llamacpp)
