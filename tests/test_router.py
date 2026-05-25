from llm.routing.router import (
    LLMRouter
)


class FakeProvider:

    def name(self):
        return "fake"


router = LLMRouter()

router.register(
    FakeProvider()
)

provider = router.get()

print(
    provider.name()
)
