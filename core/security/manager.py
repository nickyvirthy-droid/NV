"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Security Manager

Descrição: Ponto central de validação de segurança.
           Suporta enforcement configurável (compatibility | soft | strict).

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path
import yaml

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
from core.security.models import (
    SecurityDecision
)


class SecurityManager:

    def __init__(
        self,
        enforcement_path: str | Path | None = None,
        permissions_path: str | Path | None = None,
        scopes_path: str | Path | None = None,
        approval_path: str | Path | None = None
    ):

        self.enforcement_path = Path(
            enforcement_path or "config/security/enforcement.yaml"
        )

        self.policy_engine = PolicyEngine()
        self.permission_engine = PermissionEngine(permissions_path)
        self.scope_engine = ScopeEngine(scopes_path)
        self.approval_engine = ApprovalEngine(approval_path)
        self.audit_engine = AuditEngine()

        self._enforcement: dict | None = None

    def _load_enforcement(self) -> dict:

        if self._enforcement is not None:
            return self._enforcement

        defaults = {
            "mode": "compatibility",
            "policy": True,
            "permission": True,
            "scope": True,
            "approval": False,
            "fail_closed": True,
            "default_role": "admin"
        }

        if not self.enforcement_path.exists():
            self._enforcement = defaults
            return self._enforcement

        with open(self.enforcement_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        cfg = data.get("enforcement", {})
        self._enforcement = {**defaults, **cfg}
        return self._enforcement

    def reload(self) -> None:
        """Recarrega todos os YAMLs de configuração."""
        self._enforcement = None
        self.permission_engine.reload()
        self.scope_engine.reload()
        self.approval_engine.reload()
        self._load_enforcement()

    def get_mode(self) -> str:
        return self._load_enforcement().get("mode", "compatibility")

    async def validate(
        self,
        action_name: str,
        payload: dict | None = None,
        role: str | None = None
    ) -> SecurityDecision:

        payload = payload or {}
        cfg = self._load_enforcement()

        mode = cfg.get("mode", "compatibility")
        role = role or cfg.get("default_role", "admin")
        fail_closed = cfg.get("fail_closed", True)

        # ------------------------------------------------------------------
        # Policy Layer
        # ------------------------------------------------------------------
        if cfg.get("policy", True):
            policy = await self.policy_engine.validate(
                action_name=action_name,
                payload=payload,
                mode=mode
            )
            if not policy.allowed:
                await self.audit_engine.record(
                    action_name=action_name,
                    allowed=False,
                    reason=policy.reason,
                    mode=mode,
                    engine="policy"
                )
                if mode == "strict" and fail_closed:
                    return policy
                # soft → continua (apenas auditou)

        # ------------------------------------------------------------------
        # Permission Layer
        # ------------------------------------------------------------------
        if cfg.get("permission", True):
            permission = await self.permission_engine.validate(
                action_name=action_name,
                role=role,
                mode=mode
            )
            if not permission.allowed:
                await self.audit_engine.record(
                    action_name=action_name,
                    allowed=False,
                    reason=permission.reason,
                    mode=mode,
                    engine="permission"
                )
                if mode == "strict" and fail_closed:
                    return permission

        # ------------------------------------------------------------------
        # Scope Layer
        # ------------------------------------------------------------------
        if cfg.get("scope", True):
            scope = await self.scope_engine.validate(
                action_name=action_name,
                payload=payload,
                mode=mode
            )
            if not scope.allowed:
                await self.audit_engine.record(
                    action_name=action_name,
                    allowed=False,
                    reason=scope.reason,
                    mode=mode,
                    engine="scope"
                )
                if mode == "strict" and fail_closed:
                    return scope

        # ------------------------------------------------------------------
        # Approval Layer (desativado por padrão nesta fase)
        # ------------------------------------------------------------------
        approval_enabled = cfg.get("approval", False)
        approval = await self.approval_engine.validate(
            action_name=action_name,
            payload=payload,
            mode=mode,
            approval_enabled=approval_enabled
        )
        if not approval.allowed:
            await self.audit_engine.record(
                action_name=action_name,
                allowed=False,
                reason=approval.reason,
                mode=mode,
                engine="approval"
            )
            if mode == "strict" and fail_closed:
                return approval

        # ------------------------------------------------------------------
        # Sucesso
        # ------------------------------------------------------------------
        final = SecurityDecision(
            allowed=True,
            reason="validated",
            engine="manager",
            mode=mode
        )

        await self.audit_engine.record(
            action_name=action_name,
            allowed=True,
            reason=final.reason,
            mode=mode,
            engine="manager"
        )

        return final
