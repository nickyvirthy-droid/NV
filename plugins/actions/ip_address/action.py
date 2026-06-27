"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: IP Address Action

Descrição: Retorna informações de rede.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import socket

from core.actions.base import BaseAction


class IpAddressAction(BaseAction):

    name = "ip_address"

    description = (
        "Retorna informações "
        "de rede."
    )

    async def execute(
        self,
        context,
        payload
    ):

        hostname = socket.gethostname()

        return {

            "hostname":
                hostname,

            "local_ip":
                socket.gethostbyname(
                    hostname
                ),
        }
