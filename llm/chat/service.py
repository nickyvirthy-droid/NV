class ChatService:
    def __init__(
        self,
        provider,
    ):
        self.provider = provider

    async def chat(
        self,
        message,
    ):
        response = await self.provider.chat(
            message,
        )

        return {
            "message": response,
        }
