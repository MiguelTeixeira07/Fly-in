from typing import Optional as Opt
from graph import Graph
from collections import deque


class Solution:
    class Path:
        class PathNode:
            def __init__(self, data: Graph.Node | Graph.Connection) -> None:
                self.node: Graph.Node | Graph.Connection = data
                self.possibilities: list[Solution.Path.PathNode] = []

        def __init__(self, paths: list[list[Graph.Node, Graph.Connection]]):
            self.root: Solution.Path.PathNode = self.PathNode(paths[0][0])

            for path in paths:
                current: Solution.Path.PathNode = self.root

                for node in path[1:]:
                    next_node: Opt[Solution.Path.PathNode] = None

                    for possibility in current.possibilities:
                        if possibility.node == node:
                            next_node = possibility
                            break

                    if next_node is None:
                        next_node = self.PathNode(node)
                        current.possibilities.append(next_node)

                    current = next_node

        def print_paths(self) -> None:
            def print_node(node: Solution.Path.PathNode) -> None:
                possibilities = ', '.join(
                    possibility.node.name
                    for possibility in node.possibilities
                )

                print(f'{node.node.name} - {possibilities}\n')

                for possibility in node.possibilities:
                    print_node(possibility)

            print_node(self.root)


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
                if candidate.get_opposite_node(node) not in visited and candidate.get_opposite_node(node).weight < 3:
                    visited.add(candidate.get_opposite_node(node))

                    queue.append((
                        candidate.get_opposite_node(node),
                        path + [candidate.get_opposite_node(node)],
                    ))

        return []

    @staticmethod
    def get_weight_sum(path: list[Graph.Node | Graph.Connection]) -> int:
        weight_sum: int = 0

        for node in path:
            if not isinstance(node, Graph.Connection):
                weight_sum += node.weight

        return weight_sum

    @staticmethod
    def path(graph: Graph) -> Solution.Path:
        shortest_length = Solution.get_weight_sum(
            Solution.breadth_first_search(graph)
        )

        start = graph.start

        queue = [(start, [start])]
        paths: list[list[Graph.Node]] = []

        while queue:
            node, current_path = queue.pop()

            current_weight = Solution.get_weight_sum(current_path)

            if current_weight > shortest_length:
                continue

            if node == graph.goal:
                if current_weight == shortest_length:
                    paths.append(current_path)
                continue

            if isinstance(node, Graph.Connection):
                continue

            for connection in node.connections:
                candidate = connection.get_opposite_node(node)

                if candidate in current_path or candidate.weight == 3:
                    continue


                if Solution.get_weight_sum(current_path) <= shortest_length:
                    if candidate.weight == 2:
                        queue.append((candidate, current_path + [connection, candidate]))
                        continue
                    queue.append((candidate, current_path + [candidate]))

        return Solution.Path(paths)
