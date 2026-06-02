from core.runtime.kernel import RuntimeKernel

kernel = RuntimeKernel()

print(
    kernel.actions.registry.list()
)
