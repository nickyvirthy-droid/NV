"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: llama.cpp Provider

Descrição: Provider local baseado em llama.cpp server.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import httpx

from llm.providers.base import BaseProvider
from llm.providers.request import ProviderRequest
from llm.providers.response import ProviderResponse
from llm.prompts.builder import PromptBuilder

class LlamaCppProvider(BaseProvider):

    name = "llamacpp"

    def __init__(
        self,
        base_url="http://localhost:8081",
        model="Qwen2.5-3B-Instruct-Q4_K_M"
    ):

        self.base_url = base_url

        self.model = model

    async def generate(
        self,
        request: ProviderRequest
    ) -> ProviderResponse:

        prompt = PromptBuilder.build(
            request.messages
        )

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{self.base_url}/completion",
                json={
                    "prompt": prompt,
                    "temperature": request.temperature,
                    "n_predict": request.max_tokens,
                    "stop": [
                        "<|im_end|>"
                    ]
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            return ProviderResponse(
                content=data["content"].strip(),
                provider=self.name,
                success=True
            )

    async def healthcheck(self):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.base_url}/health"
            )

            return response.status_code == 200
