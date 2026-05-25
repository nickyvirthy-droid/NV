from pathlib import Path

from core.capabilities.runtime_context import (
    build_runtime_context
)


class PromptBuilder:

    def __init__(
        self,
        runtime,
        session=None,
    ):

        self.runtime = runtime

        self.session = session

    def build_system_prompt(self):

        system_prompt = Path(
            "llm/prompts/system.txt"
        ).read_text()

        capabilities = (
            self.runtime.action_registry
            .list_actions()
        )

        capability_lines = []

        for action in capabilities:

            capability_lines.append(
                f"- {action.name}: "
                f"{action.description}"
            )

        capabilities_text = "\n".join(
            capability_lines
        )

        runtime_context = ""

        if self.session:

            context = (
                build_runtime_context(
                    self.session
                )
            )

            runtime_context = (
                "\n".join(
                    [
                        f"{k}: {v}"
                        for k, v in (
                            context.items()
                        )
                    ]
                )
            )

        return (
            f"{system_prompt}\n\n"

            f"Runtime Context:\n"
            f"{runtime_context}\n\n"

            f"Current capabilities:\n"
            f"{capabilities_text}"
        )
