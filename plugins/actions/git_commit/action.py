from core.actions.base import (
    BaseAction
)

from core.coder import (
    GitManager
)


class GitCommitAction(BaseAction):

    name = "git_commit"

    description = (
        "Executa commit git."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        payload = payload or {}

        message = payload.get(
            "message",
            "NV Commit"
        )

        git = GitManager()

        return git.commit(
            message
        )
