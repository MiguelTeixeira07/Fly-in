from time import sleep
from graph import Graph
from typing import Optional as Opt
from solution import Solution


class Simulation:
    class Drone:
        location: Solution.Path.PathNode

        def __init__(self, number: int) -> None:
            self.visited: list[Graph.Node] = []
            self.number: int = number

        def move(self, dest: Solution.Path.PathNode):
            self.visited.append(self.location)
            if isinstance(self.location.node, Graph.Node) and isinstance(dest.node, Graph.Node):
                connection: Graph.Connection = Simulation.graph.get_connection_by_nodes(self.location.node, dest.node)
                connection.drones_passed += 1

            self.location.node.drones.remove(self)
            self.location = dest
            self.location.node.drones.append(self)

    @classmethod
    def __init__(cls, graph: Graph, n_drones: int) -> None:
        cls.graph: Graph = graph
        cls.n_drones: int = n_drones
        cls.drones: list['Simulation.Drone'] = []

        for i in range(cls.n_drones):
            new_drone = Simulation.Drone(i)
            new_drone.location = cls.graph.start
            cls.drones.append(new_drone)
            cls.graph.start.drones.append(new_drone)

    @classmethod
    def start(cls) -> list[list[Graph.Node | Graph.Connection]]:
        path: Solution.Path = Solution.path(cls.graph)
        output: list[list[Graph.Node]] = [[] for _ in cls.drones]

        for drone in cls.drones:
            drone.location = path.root

        while len(cls.graph.goal.drones) < cls.n_drones:
            cls.graph.clear_connections()
            for drone in cls.drones:
                for possibility in drone.location.possibilities:
                    if len(possibility.node.drones) >= possibility.node.max_drones:
                        continue
                    if isinstance(drone.location.node, Graph.Node) and isinstance(possibility.node, Graph.Node):
                        connection: Graph.Connection = cls.graph.get_connection_by_nodes(drone.location.node, possibility.node)
                        if connection.drones_passed >= connection.max_drones:
                            continue

                    drone.move(possibility)
                    break

                output[drone.number].append(drone.location.node)

        return output
