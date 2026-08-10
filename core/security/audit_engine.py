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

    def __init__(self):
        # Memória temporária (persistência em banco virá depois)
        self._records: list[AuditRecord] = []

    async def record(
        self,
        action_name: str,
        allowed: bool,
        reason: str | None = None,
        mode: str | None = None,
        engine: str | None = None
    ) -> AuditRecord:

        record = AuditRecord(
            timestamp=datetime.now(UTC),
            action_name=action_name,
            allowed=allowed,
            reason=reason,
            mode=mode,
            engine=engine
        )

        self._records.append(record)
        return record

    def get_records(self) -> list[AuditRecord]:
        return list(self._records)

    def clear(self) -> None:
        self._records.clear()
