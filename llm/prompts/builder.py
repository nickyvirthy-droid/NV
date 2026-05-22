from pathlib import Path


class PromptBuilder:
    def __init__(
        self,
        runtime,
    ):
        self.runtime = runtime

    def build_system_prompt(self):
        system_prompt = Path(
            "llm/prompts/system.txt"
        ).read_text()

        capabilities = (
            self.runtime.action_registry
            .list_actions()
        )

        capability_lines = []

        for name, data in (
            capabilities.items()
        ):
            capability_lines.append(
                f"- {name}: "
                f"{data['description']}"
            )

        capabilities_text = "\n".join(
            capability_lines
        )

        return (
            f"{system_prompt}\n\n"
            f"Current capabilities:\n"
            f"{capabilities_text}"
        )
