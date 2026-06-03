"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Uptime Formatter

Descrição: Formata uptime.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

def format_uptime(data):

    seconds = data["seconds"]

    days = seconds // 86400

    hours = (seconds % 86400) // 3600

    minutes = (seconds % 3600) // 60

    return (
        f"Uptime:\n"
        f"{days} dias\n"
        f"{hours} horas\n"
        f"{minutes} minutos"
    )
