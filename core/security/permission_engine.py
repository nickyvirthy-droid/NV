"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Permission Engine

Descrição: Controle de permissões por role.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path
import yaml

from core.security.models import (
    SecurityDecision
)


class PermissionEngine:

    def __init__(self, config_path: str | Path | None = None):

        self.config_path = Path(
            config_path or "config/security/permissions.yaml"
        )
        self._config: dict | None = None

    def _load_config(self) -> dict:

        if self._config is not None:
            return self._config

        if not self.config_path.exists():
            # Fallback seguro: sem arquivo = tudo permitido
            self._config = {"roles": {}, "actions": {}}
            return self._config

        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}

        return self._config

    def reload(self) -> None:
        """Força recarga do YAML (útil em testes e hot-reload)."""
        self._config = None
        self._load_config()

    async def validate(
        self,
        action_name: str,
        role: str = "admin",
        mode: str = "compatibility"
    ) -> SecurityDecision:

        if mode == "compatibility":
            return SecurityDecision(
                allowed=True,
                reason="compatibility_mode",
                engine="permission",
                mode=mode
            )

        config = self._load_config()
        actions = config.get("actions", {})
        roles = config.get("roles", {})

        required_level = actions.get(action_name)

        # Ação não mapeada → trata como liberada (evolução segura)
        if required_level is None:
            return SecurityDecision(
                allowed=True,
                reason=f"action_not_mapped:{action_name}",
                engine="permission",
                mode=mode
            )

        role_data = roles.get(role, {})
        role_permissions = set(role_data.get("permissions", []))

        # Hierarquia simples
        level_order = {"read": 1, "write": 2, "admin": 3}
        required_rank = level_order.get(required_level, 99)

        has_permission = False
        for perm in role_permissions:
            if level_order.get(perm, 0) >= required_rank:
                has_permission = True
                break

        if has_permission:
            return SecurityDecision(
                allowed=True,
                reason=f"role={role} level={required_level}",
                engine="permission",
                mode=mode
            )

        return SecurityDecision(
            allowed=False,
            reason=(
                f"permission_denied: role={role} "
                f"requires={required_level} action={action_name}"
            ),
            engine="permission",
            mode=mode
        )
