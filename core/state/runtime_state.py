"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Runtime State

Descrição: Estado global do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

class RuntimeState:

    def __init__(self):

        self.started = False
        self.providers = {}
        self.workflows = {}
        self.sessions = {}
