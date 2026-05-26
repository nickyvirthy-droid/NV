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


async def main():

    logger.info("NV Runtime booting")

    kernel = RuntimeKernel()

    await kernel.boot()

    logger.info("NV Runtime online")


if __name__ == "__main__":
    asyncio.run(main())
