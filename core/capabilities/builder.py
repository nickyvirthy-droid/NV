def build_capabilities(registry):

    lines = []

    for action in registry.list():

        lines.append(
            f"- {action.name}: {action.description}"
        )

    return "\n".join(lines)
