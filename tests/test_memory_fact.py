from core.memory.facts import (
    MemoryFact
)

fact = MemoryFact(
    namespace="profile",
    key="name",
    value="Alex"
)

print(fact.namespace)

print(fact.key)

print(fact.value)
