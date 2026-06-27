"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Git Checkout Action

Descrição: Troca branch.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitCheckoutAction(BaseAction):

    name = "git_checkout"

    description = (
        "Executa git checkout."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        branch = payload.get(
            "branch"
        )

        git = GitManager()

        return git.checkout(
            branch
        )
