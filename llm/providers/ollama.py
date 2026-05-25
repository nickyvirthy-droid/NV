from llm.providers.base import (
    BaseProvider
)


class OllamaProvider(
    BaseProvider
):

    def __init__(
        self,
        client,
    ):
        self.client = client

    async def generate(
        self,
        prompt: str,
    ):

        return await self.client.generate(
            prompt
        )

    async def health(self):

        return {
            "status": "ok"
        }

    def name(self):

        return "ollama"
