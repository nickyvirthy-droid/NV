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

    db.execute_commit(
        """
        CREATE TABLE IF NOT EXISTS nv_messages (

            id BIGINT AUTO_INCREMENT PRIMARY KEY,

            owner_id VARCHAR(128) NOT NULL,

            source VARCHAR(32) NOT NULL,

            role VARCHAR(32) NOT NULL,

            content LONGTEXT NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            INDEX idx_owner (
                owner_id
            ),

            INDEX idx_created (
                created_at
            )

        )
        """
    )

    db.execute_commit(
        """
        CREATE TABLE IF NOT EXISTS nv_workflow_executions (

            execution_id VARCHAR(128)
            PRIMARY KEY,

            workflow_id VARCHAR(128)
            NOT NULL,

            status VARCHAR(32)
            NOT NULL,

            results LONGTEXT,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    print(
        "Migration executed."
    )
