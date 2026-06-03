from core.runtime.kernel import RuntimeKernel

kernel = RuntimeKernel()

memory = kernel.container.resolve(
    "memory"
)

memory.profile.set_name(
    "Alex"
)

print(
    memory.profile.get_name()
)
