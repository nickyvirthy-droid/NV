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
from plugins.actions.datetime.action import (
    DatetimeAction
)
from plugins.actions.uptime.action import (
    UptimeAction
)

def register_actions(manager):

    manager.registry.register(
        SystemInfoAction()
    )

    manager.registry.register(
        DatetimeAction()
    )

    manager.registry.register(
        UptimeAction()
    )
