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
        shortest_length: int = Solution.get_weight_sum(Solution.breadth_first_search(graph))
        start: Graph.Node = graph.start
        
        queue: list[tuple[Graph.Node, list[Graph.Node]]] = []
        visited: dict[Graph.Node, int] = {}
        definite_path: list[Graph.Node] = []

        queue.append((start, [start]))

        path_weight: int = 0

        while queue:
            node, path = queue.pop()
            visited[node] = Solution.get_weight_sum(path)
            path_weight += node.weight
            if node == graph.goal and Solution.get_weight_sum(path) <= shortest_length:
                definite_path = path

            for candidate in node.connections:
                if (
                    candidate[0] not in visited.keys() or
                    (candidate[0] in visited.keys() and
                    Solution.get_weight_sum(path + [candidate[0]]) < visited[candidate[0]]) and
                    Solution.get_weight_sum(path) < shortest_length
                ):
                    queue.append((
                        candidate[0],
                        path + [candidate[0]],
                    ))

        return definite_path
