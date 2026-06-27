from core.actions.registry import (
    ActionRegistry
)

registry = ActionRegistry()

print(
    isinstance(
        registry._actions,
        dict
    )
)

print(
    len(
        registry._actions
    )
)
