"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Workflow Executions Repository

Descrição: Persistência de execuções de workflows.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import json


class WorkflowExecutionsRepository:

    def __init__(
        self,
        database
    ):

        self.database = database

    def save(
        self,
        execution
    ):

        self.database.execute_commit(
            """
            INSERT INTO nv_workflow_executions
            (
                execution_id,
                workflow_id,
                status,
                results
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            ON DUPLICATE KEY UPDATE

                status = VALUES(status),

                results = VALUES(results)
            """,
            (
                execution.execution_id,
                execution.workflow_id,
                execution.status,
                json.dumps(
                    execution.results
                )
            )
        )

    def get(
        self,
        execution_id: str
    ):

        return self.database.fetchone(
            """
            SELECT *
            FROM nv_workflow_executions
            WHERE execution_id = %s
            """,
            (
                execution_id,
            )
        )

    def list(
        self,
        limit: int = 50
    ):

        return self.database.fetchall(
            """
            SELECT *
            FROM nv_workflow_executions
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (
                limit,
            )
        )

    def count(self):

        result = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM nv_workflow_executions
            """
        )

        return result["total"]
