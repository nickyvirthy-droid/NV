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


class RuntimeKernel:

    def __init__(self):

        self.container = ServiceContainer()
        self.events = EventBus()

    async def boot(self):

        await self.events.emit(
            "SYSTEM_BOOT",
            {"status": "initializing"}
        )

    async def shutdown(self):

        await self.events.emit(
            "SYSTEM_SHUTDOWN",
            {"status": "stopping"}
        )
