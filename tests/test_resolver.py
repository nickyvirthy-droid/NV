from core.actions.resolver.resolver import (
    ActionResolver
)

resolver = ActionResolver()

print(
    resolver.resolve(
        "me mostre informações do sistema"
    )
)

print(
    resolver.resolve(
        "qual a versão do python"
    )
)

print(
    resolver.resolve(
        "bom dia"
    )
)
