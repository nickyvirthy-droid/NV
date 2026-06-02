"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Context

Descrição: Contexto de execução das actions.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass


@dataclass
class ActionContext:

    kernel: object

    session: object | None = None

    metadata: dict | None = None
