from collections.abc import Callable


class Graph:
    class Node:
        def __init__(self, name: str, zone_type: str) -> None:
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

            self.connections: list['Graph.Node'] = []


    def __init__(
            self,
            names: list[str],
            zone_types: list[str],
            connections: list[str]
        ) -> None:
        nodes: list['Graph.Node'] = []
        get_node_by_name: Callable[[str], 'Graph.Node'] = lambda name: next(
            nodes[(i for i, node in enumerate(nodes) if node.name == name)]
        )

        for name, zone_type in names, zone_types:
            new_node = Graph.Node(name, zone_type)
            nodes.append(new_node)

        for connection in connections:
            node1_name, node2_name = connection.split('-')
            node1 = get_node_by_name(node1_name)
            node2 = get_node_by_name(node2_name)
            node1.connections.append(node2)
            node2.connections.append(node1)
