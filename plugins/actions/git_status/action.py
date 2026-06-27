from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitStatusAction(BaseAction):

    name = "git_status"

    description = (
        "Retorna status do git."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        git = GitManager()

        return {
            "status": git.status()
        }
