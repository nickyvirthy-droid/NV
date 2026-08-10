"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Security Models

Descrição: Modelos da Security Layer.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass


@dataclass
class SecurityDecision:

    allowed: bool = True

    reason: str | None = None

    engine: str | None = None

    mode: str | None = None
