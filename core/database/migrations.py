"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Database Migrations

Descrição: Criação das tabelas do NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.database.manager import DatabaseManager


def run_migrations():

    db = DatabaseManager()

    db.execute_commit(
        """
        CREATE TABLE IF NOT EXISTS nv_key_value (

            id INT AUTO_INCREMENT PRIMARY KEY,

            namespace VARCHAR(100) NOT NULL,

            item_key VARCHAR(255) NOT NULL,

            item_value TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,

            UNIQUE KEY uk_namespace_key (
                namespace,
                item_key
            )

        )
        """
    )

    print(
        "Migration executed."
    )
