"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Runtime Config

Descrição: Configurações centrais do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from dataclasses import dataclass


@dataclass
class RuntimeConfig:

    environment: str = "development"

    debug: bool = True

    plugins_dir: str = "plugins"

    owner_id: str = "alex"

    history_limit: int = 50
