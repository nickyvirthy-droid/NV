"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Scope Engine

Descrição: Validação de escopo operacional.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path
import yaml

from core.security.models import (
    SecurityDecision
)


class ScopeEngine:

    def __init__(self, config_path: str | Path | None = None):

        self.config_path = Path(
            config_path or "config/security/scopes.yaml"
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
        mode: str = "compatibility"
    ) -> SecurityDecision:

        if mode == "compatibility":
            return SecurityDecision(
                allowed=True,
                reason="compatibility_mode",
                engine="scope",
                mode=mode
            )

        payload = payload or {}
        config = self._load_config()

        # --- Filesystem paths ---
        if action_name.startswith("filesystem_"):
            path = (
                payload.get("path")
                or payload.get("target")
                or payload.get("src")
            )
            if path:
                allowed_paths = (
                    config.get("filesystem", {})
                    .get("allowed_paths", [])
                )
                if allowed_paths:
                    path_str = str(path)
                    if not any(
                        path_str.startswith(str(p))
                        for p in allowed_paths
                    ):
                        return SecurityDecision(
                            allowed=False,
                            reason=(
                                f"scope_denied: path={path_str} "
                                f"not in allowed_paths"
                            ),
                            engine="scope",
                            mode=mode
                        )

        # --- system_exec commands ---
        if action_name == "system_exec":
            command = payload.get("command") or payload.get("cmd")
            if command:
                allowed_cmds = (
                    config.get("system_exec", {})
                    .get("allowed_commands", [])
                )
                if allowed_cmds:
                    # Pega o primeiro token do comando
                    cmd_token = str(command).strip().split()[0]
                    if cmd_token not in allowed_cmds:
                        return SecurityDecision(
                            allowed=False,
                            reason=(
                                f"scope_denied: command={cmd_token} "
                                f"not in allowed_commands"
                            ),
                            engine="scope",
                            mode=mode
                        )

        # --- database tables ---
        if action_name.startswith("db_") or action_name.startswith("database_"):
            table = payload.get("table")
            if table:
                allowed_tables = (
                    config.get("database", {})
                    .get("allowed_tables", [])
                )
                if allowed_tables and table not in allowed_tables:
                    return SecurityDecision(
                        allowed=False,
                        reason=(
                            f"scope_denied: table={table} "
                            f"not in allowed_tables"
                        ),
                        engine="scope",
                        mode=mode
                    )

        return SecurityDecision(
            allowed=True,
            reason="scope_ok",
            engine="scope",
            mode=mode
        )
