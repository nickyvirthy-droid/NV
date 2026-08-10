"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Audit Models

Descrição: Modelos de auditoria da Security Layer.

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

    mode: str | None = None

    engine: str | None = None
