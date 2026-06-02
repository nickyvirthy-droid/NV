from core.runtime.kernel import RuntimeKernel

kernel = RuntimeKernel()

db = kernel.container.resolve(
    "database"
)

result = db.fetchone(
    "SELECT VERSION() AS version"
)

print(result)
