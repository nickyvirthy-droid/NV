"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Provider Manager

Descrição: Gerenciador central de providers do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from llm.providers.base import BaseProvider


class ProviderManager:

    def __init__(self):

        self.providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider):

        self.providers[provider.name] = provider

    def get(self, name: str):

        return self.providers[name]

    def all(self):

        return self.providers
