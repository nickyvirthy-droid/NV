"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Permission Engine

Descrição: Controle de permissões por role.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.security.models import (
    SecurityDecision
)


class PermissionEngine:

    async def validate(
        self,
        action_name: str,
        role: str = "admin"
    ) -> SecurityDecision:

        #
        # Fase 2
        #
        # Compatibilidade total.
        #
        # Enquanto não existir
        # autenticação de usuários,
        # o Runtime opera como admin.
        #

        return SecurityDecision(
            allowed=True
        )
