from typing import Optional as Opt


class Graph:
    class Node:
        def __init__(
            self,
            name: str,
            zone_type: str,
            pos: tuple[int, int],
            max_drones: int
        ) -> None:
            from simulation import Simulation

            self.name: str = name
            match zone_type:
                case 'priority':
                    self.weight: int = 0
                case 'normal':
                    self.weight: int = 1
                case 'restricted':
                    self.weight: int = 2
                case 'blocked':
                    self.weight: int = 3

            self.pos: list[int] = list(pos)

            self.connections: list['Graph.Connection'] = []

            self.drones: list[Simulation.Drone] = []

            self.max_drones: int = max_drones


    class Connection:
        def __init__(
            self,
            name: str,
            nodes: tuple['Graph.Node', 'Graph.Node'],
            max_drones: int
        ) -> None:
            from simulation import Simulation

            self.name: str = name
            self.nodes: tuple['Graph.Node', 'Graph.Node'] = nodes
            self.max_drones: int = max_drones
            self.drones: list[Simulation.Drone] = []
            self.drones_passed: int = 0
            self.pos = ((self.nodes[0].pos[0] + self.nodes[1].pos[0]) / 2,
                        (self.nodes[0].pos[1] + self.nodes[1].pos[1]) / 2)

        def get_opposite_node(self, node: 'Graph.Node') -> 'Graph.Node':
            return self.nodes[0 if self.nodes[0] != node else 1]


    def __init__(
            self,
            names: list[str],
            zone_types: list[str],
            connections: list[tuple[str, int]],
            start: str,
            goal: str,
            positions: list[tuple[int, int]],
            max_drones: list[int]
        ) -> None:
        self.nodes: list['Graph.Node'] = []
        self.connections: list['Graph.Connection'] = []

        for name, zone_type, max_drones, pos in zip(names, zone_types, max_drones, positions):
            new_node = Graph.Node(name, zone_type, pos, max_drones)
            self.nodes.append(new_node)

        self.normalize_coords()

        for connection in connections:
            name = connection[0]
            max_drones = connection[1]
            node1_name, node2_name = connection[0].split('-')
            node1 = self.get_node_by_name(node1_name)
            node2 = self.get_node_by_name(node2_name)
            connection_object = Graph.Connection(name, (node1, node2), max_drones)
            node1.connections.append(connection_object)
            node2.connections.append(connection_object)
            self.connections.append(connection_object)

        self.start: Graph.Node = self.get_node_by_name(start)
        self.goal: Graph.Node = self.get_node_by_name(goal)


    def get_node_by_name(self, name: str) -> 'Graph.Node':
        for node in self.nodes:
            if node.name == name:
                return node

    def get_connection_by_nodes(self, node1: 'Graph.Node', node2: 'Graph.Node') -> 'Graph.Connection':
        for connection in self.connections:
            if node1.name in connection.name and node2.name in connection.name:
                return connection

    def clear_connections(self) -> None:
        for connection in self.connections:
            if len(connection.drones) > 0:
                continue

            connection.drones_passed = 0

    @staticmethod
    def graph_is_connected(graph: Graph) -> bool:
        reached_nodes: list['Graph.Node'] = []
        stack: list['Graph.Node'] = [graph.start]
        visited: list['Graph.Node'] = []

        while stack:
            node = stack.pop()
            reached_nodes.append(node)
            visited.append(node)

            for connection in node.connections:
                candidate: 'Graph.Node' = connection.get_opposite_node(node)
                if candidate not in visited:
                    stack.append(candidate)

        return len(set(reached_nodes)) == len(graph.nodes)

    def normalize_coords(self) -> 'Graph':
        min_x, min_y = self.nodes[0].pos

        for node in self.nodes:
            if node.pos[0] < min_x:
                min_x = node.pos[0]
            if node.pos[1] < min_y:
                min_y = node.pos[1]

        if min_x < 0:
            for node in self.nodes:
                node.pos[0] += abs(min_x)
        if min_x > 0:
            for node in self.nodes:
                node.pos[0] -= min_x

        if min_y < 0:
            for node in self.nodes:
                node.pos[1] += abs(min_y)
        if min_y > 0:
            for node in self.nodes:
                node.pos[1] -= min_y

        for node in self.nodes:
            node.pos[1] = abs(max(node.pos[1] for node in self.nodes) - node.pos[1])

        return self
