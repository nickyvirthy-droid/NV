"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Service Registry

Descrição: Registro e resolução de serviços do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from typing import Any


class ServiceAlreadyRegistered(Exception):
    pass


class ServiceNotFound(Exception):
    pass


class ServiceContainer:

    def __init__(self):

        self._services: dict[str, Any] = {}

    def register(self, name: str, instance: Any):

        if name in self._services:
            raise ServiceAlreadyRegistered(name)

        self._services[name] = instance

    def resolve(self, name: str):

        if name not in self._services:
            raise ServiceNotFound(name)

        return self._services[name]

    def has(self, name: str) -> bool:

        return name in self._services

    def all(self):

        return self._services
