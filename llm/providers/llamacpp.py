import httpx


class LlamaCppProvider:
    def __init__(
        self,
        base_url,
    ):
        self.base_url = base_url

    async def chat(
        self,
        system_prompt,
        user_message,
    ):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_message,
                        },
                    ],
                    "temperature": 0.7,
                    "max_tokens": 512,
                },
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0][
                "message"
            ]["content"]
