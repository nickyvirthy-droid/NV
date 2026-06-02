"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Prompt Messages

Descrição: Estruturas de mensagens do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass


@dataclass
class Message:

    role: str

    content: str
