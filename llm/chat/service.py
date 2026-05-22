from llm.prompts.builder import (
    PromptBuilder,
)


class ChatService:
    def __init__(
        self,
        provider,
        runtime,
    ):
        self.provider = provider
        self.runtime = runtime

        self.prompt_builder = (
            PromptBuilder(runtime)
        )

    async def chat(
        self,
        message,
    ):
        system_prompt = (
            self.prompt_builder
            .build_system_prompt()
        )

        response = await self.provider.chat(
            system_prompt,
            message,
        )

        action_result = (
            await self.runtime
            .action_service
            .process_response(
                response
            )
        )

        return {
            "llm_response": response,
            "action_result": action_result,
        }
