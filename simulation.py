from time import sleep
from graph import Graph
from typing import Optional as Opt
from solution import Solution
from gui import Gui


class Simulation:
    class Drone:
        location: Graph.Node
        path_index: int = 0

        def __init__(self, number: int) -> None:
            self.number: int = number

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
    def start(cls) -> list[list[Graph.Node]]:
        path: list[Graph.Node] = Solution.path(cls.graph)
        drones: list[list[Graph.Node]] = []

        for drone in cls.drones:
            drone.location = cls.graph.start

        while len(cls.graph.goal.drones) < cls.n_drones:
            for drone in cls.drones:
                if drone.number >= len(drones):
                    drones.append([])

                if len(path) > drone.path_index + 1:
                    next_node = path[drone.path_index + 1]

                if len(next_node.drones) < next_node.max_drones:
                    if drone.path_index != len(path) - 1:
                        drone.location.drones.remove(drone)
                        drone.location = next_node
                        drone.location.drones.append(drone)
                        drone.path_index += 1

                drones[drone.number].append(drone.location)


        for drone in drones:
            print('drone', drones.index(drone), '\n', ' '.join(node.name for node in drone if node.name != drone[drone.index(node)-1].name), '\n')


        return drones
