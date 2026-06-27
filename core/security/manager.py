"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Security Manager

Descrição: Ponto central de validação de segurança.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.security.policy_engine import (
    PolicyEngine
)

from core.security.permission_engine import (
    PermissionEngine
)

from core.security.scope_engine import (
    ScopeEngine
)

from core.security.approval_engine import (
    ApprovalEngine
)

from core.security.audit_engine import (
    AuditEngine
)


class SecurityManager:

    def __init__(self):

        self.policy_engine = (
            PolicyEngine()
        )

        self.permission_engine = (
            PermissionEngine()
        )

        self.scope_engine = (
            ScopeEngine()
        )

        self.approval_engine = (
            ApprovalEngine()
        )

        self.audit_engine = (
            AuditEngine()
        )

    async def validate(
        self,
        action_name: str,
        payload: dict | None = None
    ):

        payload = payload or {}

        #
        # Policy Layer
        #

        policy = await (
            self.policy_engine.validate(
                action_name=action_name,
                payload=payload
            )
        )

        if not policy.allowed:

            await self.audit_engine.record(
                action_name=action_name,
                allowed=policy.allowed,
                reason=policy.reason
            )

            return policy

        #
        # Permission Layer
        #

        permission = await (
            self.permission_engine.validate(
                action_name=action_name
            )
        )

        if not permission.allowed:

            await self.audit_engine.record(
                action_name=action_name,
                allowed=permission.allowed,
                reason=permission.reason
            )

            return permission

        #
        # Scope Layer
        #

        scope = await (
            self.scope_engine.validate(
                action_name=action_name,
                payload=payload
            )
        )

        if not scope.allowed:

            await self.audit_engine.record(
                action_name=action_name,
                allowed=scope.allowed,
                reason=scope.reason
            )

            return scope

        #
        # Approval Layer
        #

        approval = await (
            self.approval_engine.validate(
                action_name=action_name,
                payload=payload
            )
        )

        await self.audit_engine.record(
            action_name=action_name,
            allowed=approval.allowed,
            reason=approval.reason
        )

        return approval
