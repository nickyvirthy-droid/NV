"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Exec Action

Descrição: Executa comandos do sistema operacional.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import subprocess

from core.actions.base import (
    BaseAction
)


class SystemExecAction(BaseAction):

    name = "system_exec"

    description = (
        "Executa comandos do sistema."
    )

    dangerous = True

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        command = payload.get(
            "command"
        )

        if not command:

            return {
                "success": False,
                "error": "command required"
            }

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
