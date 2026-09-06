from time import sleep
from graph import Graph
from typing import Optional as Opt
from solution import Solution


class Simulation:
    class Drone:
        location: Graph.Node

        def __init__(self, number: int) -> None:
            self.visited: list[Graph.Node] = []
            self.number: int = number

        def move(self, dest: Graph.Node):
            self.visited.append(self.location)
            self.location.drones.remove(self)
            self.location = dest
            self.location.drones.append(self)

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
        output: list[list[Graph.Node]] = [[] for _ in cls.drones]

        for drone in cls.drones:
            drone.location = cls.graph.start

        while len(cls.graph.goal.drones) < cls.n_drones:
            print()
            for drone in cls.drones:
                print('\n')
                if drone.location == Simulation.graph.goal:
                    output[drone.number].append(drone.location)
                    continue

                for node in drone.location.connections:
                    print(node[1])
                    if node[0] not in path or len(node[0].drones) == node[0].max_drones:
                        continue

                    if node[0] not in drone.visited:
                        drone.move(node[0])

                output[drone.number].append(drone.location)

        for drone in output:
            print(output.index(drone), end=': ')
            for node in drone:
                print(node.name, end=' ')
            print()

        return output
