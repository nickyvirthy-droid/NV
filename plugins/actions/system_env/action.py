"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Env Action

Descrição: Consulta variáveis de ambiente.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import os

from core.actions.base import (
    BaseAction
)


class SystemEnvAction(BaseAction):

    name = "system_env"

    description = (
        "Retorna variáveis de ambiente."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        key = payload.get(
            "key"
        )

        if key:

            return {
                "key": key,
                "value": os.getenv(
                    key
                )
            }

        return {
            "count": len(
                os.environ
            ),
            "variables": dict(
                os.environ
            )
        }
