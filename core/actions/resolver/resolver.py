"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Resolver

Descrição: Resolve mensagens para actions.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.actions.resolver.rules import (
    ACTION_RULES
)


class ActionResolver:

    def resolve(
        self,
        message: str
    ):

        message = message.lower()

        for action, keywords in ACTION_RULES.items():

            for keyword in keywords:

                if keyword in message:

                    return action

        return None
