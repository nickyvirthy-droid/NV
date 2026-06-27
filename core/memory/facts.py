"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Memory Facts

Descrição: Estrutura padronizada para fatos persistentes.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass


@dataclass(slots=True)
class MemoryFact:

    namespace: str

    key: str

    value: str
