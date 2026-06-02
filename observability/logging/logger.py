"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Logger

Descrição: Logging oficial do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import logging


logging.basicConfig(
    level=logging.INFO,
    format='[NICKY][%(levelname)s] %(asctime)s :: %(message)s'
)

logger = logging.getLogger("NV")
