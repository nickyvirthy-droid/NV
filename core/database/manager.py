"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Database Manager

Descrição: Gerenciador de banco de dados.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.database.connection import (
    DatabaseConnection
)


class DatabaseManager:

    def __init__(self):

        self.db = DatabaseConnection()

        self.connection = self.db.connect()

    def execute(
        self,
        query,
        params=None
    ):

        cursor = self.connection.cursor(
            dictionary=True
        )

        cursor.execute(
            query,
            params or ()
        )

        return cursor

    def fetchone(
        self,
        query,
        params=None
    ):

        cursor = self.execute(
            query,
            params
        )

        result = cursor.fetchone()

        cursor.close()

        return result

    def fetchall(
        self,
        query,
        params=None
    ):

        cursor = self.execute(
            query,
            params
        )

        result = cursor.fetchall()

        cursor.close()

        return result

    def execute_commit(
        self,
        query,
        params=None
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            query,
            params or ()
        )

        self.connection.commit()

        cursor.close()
