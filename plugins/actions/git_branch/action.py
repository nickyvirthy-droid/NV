"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Git Branch Action

Descrição: Retorna branch atual.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti
"""

from core.actions.base import BaseAction
from core.coder import CoderEngine


class GitBranchAction(BaseAction):

    name = "git_branch"

    description = (
        "Retorna branch atual."
    )

    async def execute(
        self,
        context,
        payload
    ):

        coder = CoderEngine()

        return {
            "branch": (
                coder.git.current_branch()
            )
        }
