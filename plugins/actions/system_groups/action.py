"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Groups Action

Descrição: Retorna grupos do usuário atual.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import os
import grp

from core.actions.base import (
    BaseAction
)


class SystemGroupsAction(BaseAction):

    name = "system_groups"

    description = (
        "Retorna grupos do usuário."
    )

    async def execute(
        self,
        context,
        payload=None
    ):

        groups = [
            grp.getgrgid(gid).gr_name
            for gid in os.getgroups()
        ]

        return {
            "groups": groups
        }
