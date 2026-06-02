"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Main

Descrição: Entrypoint principal do NV Runtime.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import asyncio

from core.runtime.kernel import RuntimeKernel
from observability.logging.logger import logger
from core.events.types import SYSTEM_BOOT
from llm.providers.request import ProviderRequest
from llm.prompts.messages import Message
from llm.system.prompt import build_system_prompt

async def boot_event(payload):

    logger.info(f"SYSTEM_BOOT :: {payload}")


async def main():

    logger.info("NV Runtime booting")

    kernel = RuntimeKernel()

    kernel.events.subscribe(
        SYSTEM_BOOT,
        boot_event
    )

    await kernel.boot()

    logger.info("NV Runtime online")

    providers = kernel.container.resolve(
        "providers"
    )

    sessions = kernel.container.resolve(
        "sessions"
    )

    session = sessions.create()

    session.messages.append(
        Message(
            role="system",
            content=build_system_prompt()
        )
    )

    session.messages.append(
        Message(
            role="user",
            content="Who are you?"
        )
    )

    llm = providers.get("llamacpp")

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

    logger.info(
        f"SESSION ID :: {session.id}"
    )

    logger.info(
        f"LLM RESPONSE :: {response.content}"
    )

if __name__ == "__main__":
    asyncio.run(main())
