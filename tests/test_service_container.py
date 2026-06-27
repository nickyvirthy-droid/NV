from core.registry.services import (
    ServiceContainer
)

container = ServiceContainer()


class MeuServico:
    pass


container.register(
    "teste",
    MeuServico()
)

print(
    container.has(
        "teste"
    )
)

service = container.resolve(
    "teste"
)

print(
    isinstance(
        service,
        MeuServico
    )
)

print(
    list(
        container.all().keys()
    )
)
