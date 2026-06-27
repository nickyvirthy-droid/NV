"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Audit Models

Descrição: Modelos da Audit Layer.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuditRecord:

    timestamp: datetime

    action_name: str

    allowed: bool

    reason: str | None = None
