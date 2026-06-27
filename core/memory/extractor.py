"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Memory Extractor

Descrição: Extrator unificado de fatos.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.memory.facts import (
    MemoryFact
)

from core.memory.resolver.profile import (
    extract_name,
    extract_city,
    extract_printer,
    extract_server,
)


def extract_facts(
    text: str
) -> list[MemoryFact]:

    facts: list[MemoryFact] = []

    name = extract_name(text)

    if name:

        facts.append(
            MemoryFact(
                namespace="profile",
                key="user_name",
                value=name
            )
        )

    city = extract_city(text)

    if city:

        facts.append(
            MemoryFact(
                namespace="profile",
                key="city",
                value=city
            )
        )

    printer = extract_printer(text)

    if printer:

        facts.append(
            MemoryFact(
                namespace="hardware",
                key="printer",
                value=printer
            )
        )

    server = extract_server(text)

    if server:

        facts.append(
            MemoryFact(
                namespace="hardware",
                key="server",
                value=server
            )
        )

    return facts
