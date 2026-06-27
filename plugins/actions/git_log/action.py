"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Git Log Action

Descrição: Histórico de commits.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitLogAction(BaseAction):

    name = "git_log"

    description = (
        "Retorna histórico git."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        limit = payload.get(
            "limit",
            10
        )

        git = GitManager()

        return {
            "log": git.log(
                limit
            )
        }
