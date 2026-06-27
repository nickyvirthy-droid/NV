"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Policy Engine

Descrição: Motor de políticas da Security Layer.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.security.models import (
    SecurityDecision
)


class PolicyEngine:

    async def validate(
        self,
        action_name: str,
        payload: dict | None = None
    ):

        return SecurityDecision(
            allowed=True
        )
