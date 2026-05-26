"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Event Bus

Descrição: Sistema de eventos do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from collections import defaultdict


class EventBus:

    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_name, callback):
        self.listeners[event_name].append(callback)

    async def emit(self, event_name, payload):

        callbacks = self.listeners.get(event_name, [])

        for callback in callbacks:
            await callback(payload)
