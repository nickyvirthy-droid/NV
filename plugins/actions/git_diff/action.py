"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Git Diff Action

Descrição: Exibe alterações locais.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitDiffAction(BaseAction):

    name = "git_diff"

    description = (
        "Retorna git diff."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        git = GitManager()

        return {
            "diff": git.diff()
        }
