"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Audit Engine

Descrição: Registro de eventos da Security Layer.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from datetime import (
    datetime,
    UTC
)
from core.security.audit_models import (
    AuditRecord
)


class AuditEngine:

    async def record(
        self,
        action_name: str,
        allowed: bool,
        reason: str | None = None
    ):

        record = AuditRecord(
            timestamp=datetime.now(UTC),
            action_name=action_name,
            allowed=allowed,
            reason=reason
        )

        return record
