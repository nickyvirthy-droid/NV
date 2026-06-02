"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Provider Request

Descrição: Estrutura de requisição para providers LLM.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass
from llm.prompts.messages import Message


@dataclass
class ProviderRequest:

    messages: list[Message]

    temperature: float = 0.7

    max_tokens: int = 512
