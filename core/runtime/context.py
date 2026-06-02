"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Runtime Context

Descrição: Contexto compartilhado do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass
from typing import Any


@dataclass
class RuntimeContext:

    kernel: Any
    state: Any
    memory: Any
    config: Any
