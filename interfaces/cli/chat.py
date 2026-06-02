"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: CLI Chat

Descrição: Interface de terminal para conversar com Nicky Virthy.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import asyncio

from core.runtime.kernel import RuntimeKernel
from core.actions.resolver.resolver import (
    ActionResolver
)
from core.actions.formatters.system_info import (
    format_system_info
)
from llm.prompts.messages import Message
from llm.providers.request import ProviderRequest

from llm.system.prompt import build_system_prompt


async def chat():

    kernel = RuntimeKernel()

    await kernel.boot()

    providers = kernel.container.resolve(
        "providers"
    )

    sessions = kernel.container.resolve(
        "sessions"
    )

    llm = providers.get("llamacpp")

    session = sessions.create()

    resolver = ActionResolver()

    session.messages.append(
        Message(
            role="system",
            content=build_system_prompt()
        )
    )

    print()
    print("====================================")
    print(" Nicky Virthy")
    print(" NV Runtime")
    print("====================================")
    print("Digite 'sair' para encerrar.")
    print()

    while True:

        user_input = input("Você > ").strip()

        if not user_input:
            continue

        if user_input.lower() in (
            "sair",
            "exit",
            "quit"
        ):
            break

        action_name = resolver.resolve(
            user_input
        )

        if action_name:

            result = await kernel.actions.execute(
                action_name
            )

            if action_name == "system_info":

                output = format_system_info(
                    result
                )

            else:

                output = str(result)

            print()
            print(f"Nicky > {output}")
            print()

            continue


        session.messages.append(
            Message(
                role="user",
                content=user_input
            )
        )

        response = await llm.generate(
            ProviderRequest(
                messages=session.messages
            )
        )

        session.messages.append(
            Message(
                role="assistant",
                content=response.content
            )
        )

        print()
        print(f"Nicky > {response.content}")
        print()

    await kernel.shutdown()


if __name__ == "__main__":
    asyncio.run(chat())
