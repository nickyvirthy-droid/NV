"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Service Container

Descrição: Container de dependências do runtime.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

class ServiceContainer:

    def __init__(self):
        self.services = {}

    def register(self, name, instance):
        self.services[name] = instance

    def resolve(self, name):
        return self.services[name]
