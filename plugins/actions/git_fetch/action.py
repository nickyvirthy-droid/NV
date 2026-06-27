"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Git Fetch Action

Descrição: Executa git fetch.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitFetchAction(BaseAction):

    name = "git_fetch"

    description = (
        "Executa git fetch."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        git = GitManager()

        return git.fetch()
