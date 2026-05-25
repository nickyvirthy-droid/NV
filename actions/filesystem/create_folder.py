from pathlib import Path

from core.registry.action_registry import (
    ActionDefinition
)

from models.actions.filesystem import (
    CreateFolderPayload
)


def execute(
    payload: CreateFolderPayload,
    workspace: Path | None = None,
):

    target = Path(payload.path)

    if workspace:
        target = workspace / payload.path

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    return {
        "success": True,
        "path": str(target)
    }


ACTION_DEFINITION = ActionDefinition(
    name="filesystem.create_folder",

    description=(
        "Create folder "
        "inside workspace"
    ),

    safe=True,

    dangerous=False,

    admin_only=False,

    requires_confirmation=False,

    category="filesystem",

    version="2.0",

    payload_model=CreateFolderPayload,

    handler=execute
)
