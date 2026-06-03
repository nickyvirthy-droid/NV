"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Memory Manager

Descrição: Gerenciador central de memórias.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.memory.profile import (
    ProfileMemory
)


class MemoryManager:

    def __init__(
        self,
        profile: ProfileMemory
    ):

        self.profile = profile
