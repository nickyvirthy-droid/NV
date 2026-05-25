import pkgutil
import importlib

import actions

from core.registry.action_registry import (
    ActionRegistry
)


def load_actions(
    registry: ActionRegistry
):

    for _, module_name, _ in (
        pkgutil.walk_packages(
            actions.__path__,
            prefix="actions."
        )
    ):

        module = importlib.import_module(
            module_name
        )

        if hasattr(
            module,
            "ACTION_DEFINITION"
        ):

            registry.register(
                module.ACTION_DEFINITION
            )
