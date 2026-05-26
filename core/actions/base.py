"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Base Action

Descrição: Contrato base para actions.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from abc import ABC, abstractmethod


class BaseAction(ABC):

    name: str
    description: str
    dangerous: bool = False

    @abstractmethod
    async def execute(self, context, payload):
        pass
