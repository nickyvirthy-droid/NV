"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Base Provider

Descrição: Contrato base para providers LLM.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):

    name: str

    @abstractmethod
    async def generate(self, request):
        pass

    @abstractmethod
    async def healthcheck(self):
        pass
