from dataclasses import dataclass
from dataclasses import field

from uuid import uuid4


@dataclass
class RuntimeSession:

    session_id: str = field(
        default_factory=lambda: str(
            uuid4()
        )
    )

    user_id: str = "default"

    workspace: str = "alex"

    provider: str = "ollama"

    admin_mode: bool = False

    memory: list = field(
        default_factory=list
    )
