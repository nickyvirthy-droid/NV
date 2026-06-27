from core.runtime.context import (
    RuntimeContext
)

context = RuntimeContext(
    kernel="kernel",
    state="state",
    memory="memory",
    config="config"
)

print(context.kernel)

print(context.state)

print(context.memory)

print(context.config)
