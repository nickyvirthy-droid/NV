class LLMRouter:

    def __init__(self):

        self.providers = {}

        self.default_provider = None

    def register(
        self,
        provider,
    ):

        self.providers[
            provider.name()
        ] = provider

        if not self.default_provider:
            self.default_provider = (
                provider.name()
            )

    def get(
        self,
        name=None,
    ):

        if not name:
            name = self.default_provider

        return self.providers.get(
            name
        )
