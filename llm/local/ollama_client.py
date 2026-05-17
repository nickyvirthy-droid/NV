import httpx

from config.settings import settings


async def generate(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False,
            },
        )

        data = response.json()

        return data["response"]
