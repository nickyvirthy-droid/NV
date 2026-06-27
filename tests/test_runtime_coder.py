from core.runtime.kernel import RuntimeKernel


kernel = RuntimeKernel()

coder = kernel.container.resolve(
    "coder"
)

print(
    coder is not None
)
