"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Process Kill Action

Descrição: Finaliza processo por PID.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import os
import signal

from core.actions.base import (
    BaseAction
)


class ProcessKillAction(BaseAction):

    name = "process_kill"

    description = (
        "Finaliza processo por PID."
    )

    dangerous = True

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        pid = payload.get(
            "pid"
        )

        if not pid:

            return {
                "success": False,
                "error": "pid required"
            }

        try:

            os.kill(
                int(pid),
                signal.SIGTERM
            )

            return {
                "success": True,
                "pid": pid
            }

        except Exception as exc:

            return {
                "success": False,
                "error": str(exc)
            }
