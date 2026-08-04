from graph import Graph
from collections import deque


class Solution:
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
                if candidate not in visited:
                    visited.add(candidate)

                    queue.append((
                        candidate,
                        path + [candidate],
                    ))

        return []

    @staticmethod
    def get_weight_sum(path: list[Graph.Node]) -> int:
        weight_sum: int = 0

        for node in path:
            weight_sum += node.weight

        return weight_sum

    @staticmethod
    def shortest_path(graph: Graph) -> list[Graph.Node]:
        shortest_length: int = Solution.get_weight_sum(Solution.breadth_first_search(graph))
        start: Graph.Node = graph.start
        
        queue: list[tuple[Graph.Node, list[Graph.Node]]] = []
        visited: set[Graph.Node] = set()
        definite_path: list[Graph.Node] = []

        queue.append((start, [start]))
        visited.add(start)

        path_weight: int = 0

        while queue:
            node, path = queue.pop()
            path_weight += node.weight
            if node == graph.goal and Solution.get_weight_sum(path) <= shortest_length:
                definite_path = path

            for candidate in node.connections:
                if candidate not in visited and Solution.get_weight_sum(path) < shortest_length:
                    visited.add(candidate)

                    queue.append((
                        candidate,
                        path + [candidate],
                    ))

        return definite_path
