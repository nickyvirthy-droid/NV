"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Approval Engine

Descrição: Controle de aprovação de ações.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path
import yaml

from core.security.models import (
    SecurityDecision
)


class ApprovalEngine:

    def __init__(self, config_path: str | Path | None = None):

        self.config_path = Path(
            config_path or "config/security/approval.yaml"
        )
        self._config: dict | None = None

    def _load_config(self) -> dict:

        if self._config is not None:
            return self._config

        if not self.config_path.exists():
            self._config = {}
            return self._config

        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}

        return self._config

    def reload(self) -> None:
        self._config = None
        self._load_config()

    async def validate(
        self,
        action_name: str,
        payload: dict | None = None,
        mode: str = "compatibility",
        approval_enabled: bool = False
    ) -> SecurityDecision:

        # Approval permanece desativado por padrão nesta fase.
        if not approval_enabled or mode == "compatibility":
            return SecurityDecision(
                allowed=True,
                reason="approval_disabled",
                engine="approval",
                mode=mode
            )

        config = self._load_config()
        action_cfg = config.get(action_name, {})

        if action_cfg.get("approval_required", False):
            # Nesta fase ainda não existe workflow de aprovação real.
            # Em strict + approval_enabled devolve denied com motivo claro.
            return SecurityDecision(
                allowed=False,
                reason=(
                    f"approval_required: action={action_name} "
                    f"(workflow de aprovação ainda não implementado)"
                ),
                engine="approval",
                mode=mode
            )

        return SecurityDecision(
            allowed=True,
            reason="approval_not_required",
            engine="approval",
            mode=mode
        )
