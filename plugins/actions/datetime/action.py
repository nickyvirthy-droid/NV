"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Datetime Action

Descrição: Retorna data e hora atual.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from datetime import datetime

from core.actions.base import BaseAction


class DatetimeAction(BaseAction):

    name = "datetime"

    description = (
        "Retorna data e hora atual."
    )

    async def execute(
        self,
        context,
        payload
    ):

        now = datetime.now()

        return {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M:%S"),
        }
