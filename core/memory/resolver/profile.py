"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Profile Resolver

Descrição: Resolve intenções relacionadas ao perfil.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import re


def extract_name(text: str):

    patterns = [

        r"meu nome é (.+)",

        r"meu nome e (.+)",

        r"eu sou (.+)",
    ]

    text = text.lower().strip()

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            return match.group(1).strip().title()

    return None


def is_name_question(text: str):

    text = text.lower().strip()

    triggers = [

        "qual meu nome",

        "qual é meu nome",

        "qual e meu nome",

        "você sabe meu nome",

        "voce sabe meu nome",

        "quem sou eu",

        "quem eu sou",

        "sabe quem eu sou",
    ]

    return any(
        trigger in text
        for trigger in triggers
    )
