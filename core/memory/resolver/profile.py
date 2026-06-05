"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Profile Resolver

Descrição: Extração e consulta de informações do perfil.

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


def extract_city(text: str):

    patterns = [

        r"moro em (.+)",

        r"sou de (.+)",

        r"minha cidade é (.+)",

        r"minha cidade e (.+)",
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


def extract_printer(text: str):

    patterns = [

        r"tenho uma impressora (.+)",

        r"minha impressora é (.+)",

        r"minha impressora e (.+)",
    ]

    text = text.strip()

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return None


def extract_server(text: str):

    patterns = [

        r"meu servidor é (.+)",

        r"meu servidor e (.+)",

        r"uso o servidor (.+)",
    ]

    text = text.strip()

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

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
