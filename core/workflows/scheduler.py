"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Workflow Scheduler

Descrição:
Constrói e valida DAGs de execução.

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from collections import defaultdict
from collections import deque


class WorkflowScheduler:

    def __init__(self, workflow):
        self.workflow = workflow

    def build_graph(self):

        graph = defaultdict(list)
        indegree = defaultdict(int)

        for step in self.workflow.steps:
            indegree.setdefault(
                step.step_id,
                0
            )

        for step in self.workflow.steps:

            for dep in step.dependencies:

                graph[dep].append(
                    step.step_id
                )

                indegree[
                    step.step_id
                ] += 1

        return graph, indegree

    def validate(self):

        graph, indegree = (
            self.build_graph()
        )

        queue = deque(
            [
                node
                for node, degree
                in indegree.items()
                if degree == 0
            ]
        )

        visited = []

        while queue:

            node = queue.popleft()

            visited.append(node)

            for child in graph[node]:

                indegree[child] -= 1

                if indegree[child] == 0:
                    queue.append(child)

        if len(visited) != len(indegree):
            raise ValueError(
                "Workflow DAG possui ciclos."
            )

    def build_stages(self):

        graph, indegree = (
            self.build_graph()
        )

        stages = []

        current = [
            node
            for node, degree
            in indegree.items()
            if degree == 0
        ]

        while current:

            stages.append(current)

            next_nodes = []

            for node in current:

                for child in graph[node]:

                    indegree[child] -= 1

                    if indegree[child] == 0:
                        next_nodes.append(
                            child
                        )

            current = next_nodes

        return stages
