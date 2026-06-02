"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Loader

Descrição: Registro das actions padrão.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from plugins.actions.system_info.action import (
    SystemInfoAction
)


def register_actions(manager):

    manager.registry.register(
        SystemInfoAction()
    )
