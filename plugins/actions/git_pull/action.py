"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Git Pull Action

Descrição: Executa git pull.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitPullAction(BaseAction):

    name = "git_pull"

    description = (
        "Executa git pull."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        git = GitManager()

        return git.pull()
