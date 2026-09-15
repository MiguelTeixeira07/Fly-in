from graph import Graph
from solution import Solution


class Simulation:
    class Drone:
        location: Solution.Path.PathNode

        def __init__(self, number: int) -> None:
            self.visited: list[Solution.Path.PathNode] = []
            self.number: int = number

        def move(self, dest: Solution.Path.PathNode) -> None:
            self.visited.append(self.location)
            if (
                isinstance(self.location.node, Graph.Node) and
                isinstance(dest.node, Graph.Node)
            ):
                connection: Graph.Connection = \
                    Simulation.graph.get_connection_by_nodes(
                        self.location.node, dest.node
                    )
                connection.drones_passed += 1

            self.location.node.drones.remove(self)
            self.location = dest
            self.location.node.drones.append(self)

    drones: list['Simulation.Drone']
    n_drones: int
    graph: Graph

    @classmethod
    def start(
        cls,
        graph: Graph,
        n_drones: int
    ) -> list[list[Graph.Node | Graph.Connection]]:
        cls.graph = graph
        cls.n_drones = n_drones
        cls.drones = []

        path: Solution.Path = Solution.path(cls.graph)

        for i in range(cls.n_drones):
            new_drone = Simulation.Drone(i)
            new_drone.location = path.root
            cls.drones.append(new_drone)
            cls.graph.start.drones.append(new_drone)

        output: list[
            list[
                Graph.Node | Graph.Connection
            ]
        ] = [[] for _ in cls.drones]

        for drone in cls.drones:
            drone.location = path.root

        while len(cls.graph.goal.drones) < cls.n_drones:
            cls.graph.clear_connections()
            for drone in cls.drones:
                for possibility in drone.location.possibilities:
                    if len(
                        possibility.node.drones
                    ) >= possibility.node.max_drones:
                        continue
                    if (
                        isinstance(drone.location.node, Graph.Node) and
                        isinstance(possibility.node, Graph.Node)
                    ):
                        connection: Graph.Connection = \
                            cls.graph.get_connection_by_nodes(
                                drone.location.node,
                                possibility.node
                            )
                        if connection.drones_passed >= connection.max_drones:
                            continue

                    drone.move(possibility)
                    break

                output[drone.number].append(drone.location.node)

        return output
