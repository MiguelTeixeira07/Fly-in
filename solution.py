from typing import Optional as Opt
from graph import Graph
from collections import deque


class Solution:
    class Path:
        root: Opt[Graph.Node] = None

        def __init__(self, data: Graph.Node):
            self.node: Graph.Node = data
            self.next: list[Graph.Node] = []
            
            if Solution.Path.root is None:
                Solution.Path.root = self.node


    @staticmethod
    def breadth_first_search(graph: Graph) -> list[Graph.Node]:
        start: Graph.Node = graph.start

        queue: deque[tuple[Graph.Node, list[Graph.Node]]] = deque()
        visited: set[Graph.Node] = set()

        queue.append((start, [start]))

        while queue:
            node, path = queue.popleft()

            if node == graph.goal:
                return path

            for candidate in node.connections:
                if candidate[0] not in visited:
                    visited.add(candidate[0])

                    queue.append((
                        candidate[0],
                        path + [candidate[0]],
                    ))

        return []

    @staticmethod
    def get_weight_sum(path: list[Graph.Node]) -> int:
        weight_sum: int = 0

        for node in path:
            weight_sum += node.weight

        return weight_sum

    @staticmethod
    def path(graph: Graph) -> list[Graph.Node]:
        shortest_length = Solution.get_weight_sum(
            Solution.breadth_first_search(graph)
        )

        start = graph.start

        queue = [(start, [start])]
        paths = []

        while queue:
            node, current_path = queue.pop()

            current_weight = Solution.get_weight_sum(current_path)

            if current_weight > shortest_length:
                continue

            if node == graph.goal:
                if current_weight == shortest_length:
                    paths.append(current_path)
                continue

            for connection in node.connections:
                candidate = connection[0]

                # Don't revisit nodes already in this path
                if candidate in current_path:
                    continue

                new_path = current_path + [candidate]

                if Solution.get_weight_sum(new_path) <= shortest_length:
                    queue.append((candidate, new_path))

        allowed = []

        for current_path in paths:
            for node in current_path:
                if node not in allowed:
                    allowed.append(node)

        return allowed
