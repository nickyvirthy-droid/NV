from core.runtime.kernel import (
    RuntimeKernel
)


kernel = RuntimeKernel()

memory = kernel.container.resolve(
    "memory"
)

memory.set(
    "profile",
    "city",
    "Presidente Venceslau"
)

print(
    memory.get(
        "profile",
        "city"
    )
)

print(
    memory.exists(
        "profile",
        "city"
    )
)
