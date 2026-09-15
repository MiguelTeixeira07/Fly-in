from typing import Optional as Opt
from graph import Graph
from collections import deque


class Solution:
    """Pathfinding logic for routing drones through a graph.

    Provides breadth-first search to find the shortest route between a
    graph's start and goal nodes, and a search that gathers every
    minimum-weight route into a tree structure (Path) for use during
    simulation.
    """

    class Path:
        """Tree of all minimum-weight routes from start to goal.

        Merges a list of individual routes into a shared tree so that
        drones can branch across different equally-short paths during
        simulation.

        Attributes:
            root (Solution.Path.PathNode): Root of the path tree,
                corresponding to the graph's start node.
        """

        class PathNode:
            """A single node in the path tree.

            Attributes:
                node (Graph.Node | Graph.Connection): The underlying
                    graph node or connection this tree node represents.
                possibilities (list[Solution.Path.PathNode]): Tree
                    nodes reachable from this one along a minimum-weight
                    route.
            """

            def __init__(self, data: Graph.Node | Graph.Connection) -> None:
                """Initializes a path tree node.

                Args:
                    data (Graph.Node | Graph.Connection): The graph
                        node or connection this tree node represents.
                """
                self.node: Graph.Node | Graph.Connection = data
                self.possibilities: list[Solution.Path.PathNode] = []

        def __init__(self, paths: list[list[Graph.Node | Graph.Connection]]):
            """Builds a path tree by merging a list of routes.

            Starts from the first element of the first path as the
            root, then walks each given route, reusing existing tree
            branches where routes overlap and creating new branches
            where they diverge.

            Args:
                paths (list[list[Graph.Node | Graph.Connection]]): All
                    minimum-weight routes from start to goal, each as a
                    sequence of nodes and connections.
            """
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
            """Prints the path tree to stdout.

            Recursively prints each tree node's name alongside the
            names of its possible next nodes, depth-first from the
            root.
            """
            def print_node(node: Solution.Path.PathNode) -> None:
                """Prints a single tree node and recurses into its children.

                Args:
                    node (Solution.Path.PathNode): Tree node to print.
                """
                possibilities = ', '.join(
                    possibility.node.name
                    for possibility in node.possibilities
                )

                print(f'{node.node.name} - {possibilities}\n')

                for possibility in node.possibilities:
                    print_node(possibility)

            print_node(self.root)

    @staticmethod
    def breadth_first_search(
        graph: Graph
    ) -> list[Graph.Node | Graph.Connection]:
        """Finds a shortest route from the graph's start to its goal.

        Performs a breadth-first search over nodes, skipping any node
        with a weight of 3 (blocked), and returns the first path found
        that reaches the goal node.

        Args:
            graph (Graph): Graph to search.

        Returns:
            list[Graph.Node | Graph.Connection]: Sequence of nodes
                forming a shortest route from start to goal, or an
                empty list if no route exists.
        """
        start: Graph.Node = graph.start

        queue: deque[
            tuple[
                Graph.Node,
                list[Graph.Node | Graph.Connection]
            ]
        ] = deque()
        visited: set[Graph.Node] = set()

        queue.append((start, [start]))

        while queue:
            node, path = queue.popleft()

            if node == graph.goal:
                return path

            for candidate in node.connections:
                if (
                    candidate.get_opposite_node(node) not in visited and
                    candidate.get_opposite_node(node).weight < 3
                ):
                    visited.add(candidate.get_opposite_node(node))

                    queue.append((
                        candidate.get_opposite_node(node),
                        path + [candidate.get_opposite_node(node)],
                    ))

        return []

    @staticmethod
    def get_weight_sum(path: list[Graph.Node | Graph.Connection]) -> int:
        """Sums the traversal weight of every node in a route.

        Connections are skipped since only nodes carry weight.

        Args:
            path (list[Graph.Node | Graph.Connection]): Sequence of
                nodes and connections forming a route.

        Returns:
            int: Total weight of all nodes in the route.
        """
        weight_sum: int = 0

        for node in path:
            if not isinstance(node, Graph.Connection):
                weight_sum += node.weight

        return weight_sum

    @staticmethod
    def path(graph: Graph) -> Solution.Path:
        """Finds every minimum-weight route from start to goal and merges them
        into a tree.

        First computes the shortest route's total weight via
        breadth_first_search, then explores all routes from start to
        goal, keeping only those whose total weight matches the
        shortest, inserting a connection into the route whenever a
        'restricted' (weight 2) node is entered. All qualifying routes
        are merged into a single Path tree.

        Args:
            graph (Graph): Graph to search.

        Returns:
            Solution.Path: Tree containing every minimum-weight route
                from start to goal.
        """
        shortest_length: int = Solution.get_weight_sum(
            Solution.breadth_first_search(graph)
        )

        start: Graph.Node = graph.start

        queue: list[
            tuple[
                Graph.Node | Graph.Connection,
                list[
                    Graph.Node | Graph.Connection
                ]
            ]
        ] = [(start, [start])]
        paths: list[list[Graph.Node | Graph.Connection]] = []

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
                        queue.append((
                            candidate,
                            current_path + [connection, candidate]
                        ))
                        continue
                    queue.append((candidate, current_path + [candidate]))

        return Solution.Path(paths)
