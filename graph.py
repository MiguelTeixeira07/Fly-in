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

            self.pos: tuple[int, int] = pos

            self.connections: list[tuple['Graph.Node', int]] = []

            self.drones: list[Simulation.Drone] = []

            self.max_drones: int = max_drones


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

        for name, zone_type, max_drones, pos in zip(names, zone_types, max_drones, positions):
            new_node = Graph.Node(name, zone_type, pos, max_drones)
            self.nodes.append(new_node)

        for connection in connections:
            node1_name, node2_name = connection[0].split('-')
            node1 = self.get_node_by_name(node1_name)
            node2 = self.get_node_by_name(node2_name)
            node1.connections.append((node2, connection[1]))
            node2.connections.append((node1, connection[1]))

        self.start: Graph.Node = self.get_node_by_name(start)
        self.goal: Graph.Node = self.get_node_by_name(goal)

    def get_node_by_name(self, name: str) -> 'Graph.Node':
        index: Opt[int] = None

        for i, node in enumerate(self.nodes):
            if node.name == name:
                index = i
                break

        return self.nodes[index]