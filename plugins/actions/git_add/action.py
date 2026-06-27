"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Git Add Action

Descrição: Adiciona arquivos ao stage do git.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitAddAction(BaseAction):

    name = "git_add"

    description = (
        "Executa git add."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        files = payload.get(
            "files",
            []
        )

        git = GitManager()

        return git.add(
            files
        )
