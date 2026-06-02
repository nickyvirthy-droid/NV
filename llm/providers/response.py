"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Provider Response

Descrição: Estrutura de resposta dos providers LLM.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass


@dataclass
class ProviderResponse:

    content: str

    provider: str

    success: bool = True
