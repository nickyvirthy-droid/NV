"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Prompt

Descrição: Construção do prompt central do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from llm.system.identity import RUNTIME_IDENTITY
from llm.system.policy import RUNTIME_POLICY
from llm.system.behaviors import RUNTIME_BEHAVIORS


def build_system_prompt():

    return f"""
{RUNTIME_IDENTITY}

{RUNTIME_POLICY}

{RUNTIME_BEHAVIORS}
"""
