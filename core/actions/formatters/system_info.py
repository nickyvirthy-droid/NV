"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: System Info Formatter

Descrição: Formata saída da action SystemInfo.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

def format_system_info(data):

    return f"""
Hostname: {data['hostname']}
Sistema: {data['platform']}
Python: {data['python_version']}
Runtime Ativo: {data['runtime_started']}
""".strip()
