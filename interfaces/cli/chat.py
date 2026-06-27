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
from core.memory.extractor import (
    extract_facts
)
from core.memory.resolver.profile import (
    is_name_question
)
from llm.prompts.messages import Message
from llm.providers.request import ProviderRequest
from llm.system.prompt import build_system_prompt
from core.actions.formatters.datetime import (
    format_datetime
)
from core.actions.formatters.uptime import (
    format_uptime
)


async def chat():

    kernel = RuntimeKernel()

    await kernel.boot()

    providers = kernel.container.resolve(
        "providers"
    )

    sessions = kernel.container.resolve(
        "sessions"
    )

    memory = kernel.container.resolve(
        "memory"
    )

    history = kernel.container.resolve(
        "history"
    )

    config = kernel.container.resolve(
        "config"
    )

    llm = providers.get(
        "llamacpp"
    )

    session = sessions.create()

    session.messages = history.load(
        config.owner_id,
        config.history_limit
    )

    print(
        f"[DEBUG] mensagens carregadas: {len(session.messages)}"
    )

    resolver = ActionResolver()

    session.messages.insert(
        0,
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

        user_input = input(
            "Você > "
        ).strip()

        history.save(
            config.owner_id,
            "cli",
            "user",
            user_input
        )

        if not user_input:
            continue

        if user_input.lower() in (
            "sair",
            "exit",
            "quit"
        ):
            break

        # ==================================
        # MEMORY EXTRACTION
        # ==================================

        facts = extract_facts(
            user_input
        )

        if facts:

            memory.save_facts(
                facts
            )

            print()

            for fact in facts:

                print(
                    "Nicky > Entendido. Vou lembrar disso."
                )

            print()

            continue

        # ==================================
        # MEMORY QUERIES
        # ==================================

        if is_name_question(
            user_input
        ):

            stored_name = memory.get(
                "profile",
                "user_name"
            )

            print()

            if stored_name:

                print(
                    f"Nicky > Seu nome é {stored_name}."
                )

            else:

                print(
                    "Nicky > Ainda não sei seu nome."
                )

            print()

            continue

        # ==================================
        # ACTION ENGINE
        # ==================================

        action_name = resolver.resolve(
            user_input
        )

        print(
            f"[DEBUG] action={action_name}"
        )

        if action_name:

            result = await kernel.actions.execute(
                action_name
            )

            if action_name == "system_info":

                output = format_system_info(
                    result
                )

            elif action_name == "datetime":

                output = format_datetime(
                    result
                )

            elif action_name == "uptime":

                output = format_uptime(
                    result
                )

            else:

                output = str(result)

            print()
            print(
                f"Nicky > {output}"
            )
            print()

            continue

        # ==================================
        # LLM
        # ==================================

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

        history.save(
            config.owner_id,
            "cli",
            "assistant",
            response.content
        )

        print()
        print(
            f"Nicky > {response.content}"
        )
        print()

    await kernel.shutdown()


if __name__ == "__main__":
    asyncio.run(
        chat()
    )
