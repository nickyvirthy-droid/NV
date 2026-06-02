"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Runtime Session

Descrição: Sessão operacional do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass, field
from uuid import uuid4

from llm.prompts.messages import Message


@dataclass
class Session:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    messages: list[Message] = field(
        default_factory=list
    )

    metadata: dict = field(
        default_factory=dict
    )
