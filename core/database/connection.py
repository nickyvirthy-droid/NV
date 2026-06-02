"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Database Connection

Descrição: Conexão MariaDB do NV Runtime.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import mysql.connector


class DatabaseConnection:

    def __init__(self):

        self.connection = None

    def connect(self):

        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="nicky",
            password="nicky_senha_123",
            database="nicky_db"
        )

        return self.connection
