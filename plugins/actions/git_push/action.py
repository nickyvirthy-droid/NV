"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Git Push Action

Descrição: Executa git push.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitPushAction(BaseAction):

    name = "git_push"

    description = (
        "Executa git push."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        git = GitManager()

        return git.push()
