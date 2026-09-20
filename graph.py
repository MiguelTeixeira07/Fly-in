class Graph:
    """Graph representation of a parsed map.

    Builds a graph of nodes (hubs) and connections (links) from parsed
    map data, normalizes node coordinates, and exposes helpers for
    lookups and connectivity checks used by the solver and simulation.

    Attributes:
        nodes (list[Graph.Node]): All nodes in the graph.
        connections (list[Graph.Connection]): All connections in the
            graph.
        start (Graph.Node): Start node of the graph.
        goal (Graph.Node): Goal node of the graph.
    """

    class Node:
        """A single node (hub) in the graph.

        Attributes:
            name (str): Name of the node.
            weight (int): Traversal cost derived from zone_type:
                0 for 'priority', 1 for 'normal', 2 for 'restricted',
                3 for 'blocked'.
            pos (list[int]): [x, y] position of the node.
            connections (list[Graph.Connection]): Connections attached
                to this node.
            drones (list[Simulation.Drone]): Drones currently occupying
                this node.
            max_drones (int): Maximum number of drones the node can
                hold at once.
        """

        def __init__(
            self,
            name: str,
            zone_type: str,
            pos: tuple[int, int],
            max_drones: int
        ) -> None:
            """Initializes a node.

            Args:
                name (str): Name of the node.
                zone_type (str): Zone type used to derive the node's
                    traversal weight ('priority', 'normal',
                    'restricted', or 'blocked').
                pos (tuple[int, int]): (x, y) position of the node.
                max_drones (int): Maximum number of drones the node can
                    hold at once.
            """
            from simulation import Simulation

            self.name: str = name
            self.weight: int = 1
            match zone_type:
                case 'priority':
                    self.weight = 0
                case 'normal':
                    self.weight = 1
                case 'restricted':
                    self.weight = 2
                case 'blocked':
                    self.weight = 3

            self.pos: list[int] = list(pos)

            self.connections: list['Graph.Connection'] = []

            self.drones: list[Simulation.Drone] = []

            self.max_drones: int = max_drones

    class Connection:
        """A single connection (edge) between two nodes in the graph.

        Attributes:
            name (str): Name of the connection, formatted as
                '<node1>-<node2>'.
            nodes (tuple[Graph.Node, Graph.Node]): The two nodes this
                connection links.
            max_drones (int): Maximum number of drones that can occupy
                this connection at once.
            drones (list[Simulation.Drone]): Drones currently occupying
                this connection.
            drones_passed (int): Number of drones that have passed
                through this connection during the current simulation
                step.
            pos (tuple[float, float]): Midpoint position between the
                two connected nodes.
        """

        def __init__(
            self,
            name: str,
            nodes: tuple['Graph.Node', 'Graph.Node'],
            max_drones: int
        ) -> None:
            """Initializes a connection between two nodes.

            Args:
                name (str): Name of the connection, formatted as
                    '<node1>-<node2>'.
                nodes (tuple[Graph.Node, Graph.Node]): The two nodes
                    this connection links.
                max_drones (int): Maximum number of drones that can
                    occupy this connection at once.
            """
            from simulation import Simulation

            self.name: str = name
            self.nodes: tuple['Graph.Node', 'Graph.Node'] = nodes
            self.max_drones: int = max_drones
            self.drones: list[Simulation.Drone] = []
            self.drones_passed: int = 0
            self.pos = ((self.nodes[0].pos[0] + self.nodes[1].pos[0]) / 2,
                        (self.nodes[0].pos[1] + self.nodes[1].pos[1]) / 2)

        def get_opposite_node(self, node: 'Graph.Node') -> 'Graph.Node':
            """Returns the node on the other end of this connection.

            Args:
                node (Graph.Node): One of the two nodes this connection
                    links.

            Returns:
                Graph.Node: The node on the opposite end from `node`.
            """
            return self.nodes[0 if self.nodes[0] != node else 1]

    def __init__(
        self,
        names: list[str],
        zone_types: list[str],
        connections: list[tuple[str, int]],
        start: str,
        goal: str,
        positions: list[tuple[int, int]],
        max_drones_l: list[int]
    ) -> None:
        """Builds a graph from parsed map data.

        Creates a node for each hub, normalizes their coordinates, then
        creates a connection for each parsed link and attaches it to
        its two endpoint nodes.

        Args:
            names (list[str]): Names of every hub.
            zone_types (list[str]): Zone type of every hub, in the same
                order as `names`.
            connections (list[tuple[str, int]]): Connection name/max
                capacity pairs, where the name is formatted as
                '<node1>-<node2>'.
            start (str): Name of the start hub.
            goal (str): Name of the goal hub.
            positions (list[tuple[int, int]]): (x, y) position of every
                hub, in the same order as `names`.
            max_drones_l (list[int]): Maximum drone capacity of every
                hub, in the same order as `names`.
        """
        self.nodes: list['Graph.Node'] = []
        self.connections: list['Graph.Connection'] = []

        for name, zone_type, max_drones, pos in zip(
            names,
            zone_types,
            max_drones_l,
            positions
        ):
            new_node = Graph.Node(name, zone_type, pos, max_drones)
            self.nodes.append(new_node)

        self.normalize_coords()

        for connection in connections:
            name = connection[0]
            max_drones = connection[1]
            node1_name, node2_name = connection[0].split('-')
            node1 = self.get_node_by_name(node1_name)
            node2 = self.get_node_by_name(node2_name)
            connection_object = Graph.Connection(
                name,
                (node1, node2),
                max_drones
            )
            node1.connections.append(connection_object)
            node2.connections.append(connection_object)
            self.connections.append(connection_object)

        self.start: 'Graph.Node' = self.get_node_by_name(start)
        self.goal: 'Graph.Node' = self.get_node_by_name(goal)

    def get_node_by_name(self, name: str) -> 'Graph.Node':
        """Finds a node by its name.

        Args:
            name (str): Name of the node to find.

        Returns:
            Graph.Node: The matching node, or the first node in the
                graph if no match is found.
        """
        for node in self.nodes:
            if node.name == name:
                return node
        return self.nodes[0]

    def get_connection_by_nodes(
        self,
        node1: 'Graph.Node',
        node2: 'Graph.Node'
    ) -> 'Graph.Connection':
        """Finds the connection linking two given nodes.

        Args:
            node1 (Graph.Node): One endpoint of the connection.
            node2 (Graph.Node): The other endpoint of the connection.

        Returns:
            Graph.Connection: The matching connection, or the first
                connection in the graph if no match is found.
        """
        for connection in self.connections:
            if (
                node1.name in connection.name and
                node2.name in connection.name
            ):
                return connection
        return self.connections[0]

    def clear_connections(self) -> None:
        """Resets the pass-through counter of unoccupied connections.

        For every connection with no drones currently on it, resets
        `drones_passed` back to 0. Connections that currently hold
        drones are left untouched.
        """
        for connection in self.connections:
            if len(connection.drones) > 0:
                continue

            connection.drones_passed = 0

    @staticmethod
    def graph_is_connected(graph: 'Graph') -> bool:
        """Checks whether every node in the graph is reachable from the start.

        Performs a depth-first traversal from the graph's start node
        and compares the number of reached nodes to the total number of
        nodes in the graph.

        Args:
            graph (Graph): Graph to check.

        Returns:
            bool: True if every node is reachable from the start node,
                False otherwise.
        """
        reached_nodes: list['Graph.Node'] = []
        stack: list['Graph.Node'] = [graph.start]
        visited: list['Graph.Node'] = []

        while stack:
            node = stack.pop()
            reached_nodes.append(node)
            visited.append(node)

            for connection in node.connections:
                candidate: 'Graph.Node' = connection.get_opposite_node(node)
                if candidate not in visited and candidate.weight != 3:
                    stack.append(candidate)

        return graph.goal in set(reached_nodes)

    def normalize_coords(self) -> None:
        """Normalizes node coordinates to start at (0, 0) and flips the Y axis.

        Shifts every node's position so that the minimum x and y values
        become 0, then flips the y-axis so that visually higher
        coordinates correspond to larger y-position values, matching
        screen-drawing conventions.

        Returns:
            Graph: This graph instance, for chaining.
        """
        min_x, min_y = self.nodes[0].pos

        for node in self.nodes:
            if node.pos[0] < min_x:
                min_x = node.pos[0]
            if node.pos[1] < min_y:
                min_y = node.pos[1]

        for node in self.nodes:
            node.pos[0] -= min_x
            node.pos[1] -= min_y
