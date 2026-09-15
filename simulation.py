from graph import Graph
from solution import Solution


class Simulation:
    """Drives drones through the graph along the precomputed path tree.

    Simulates `n_drones` moving step by step from the graph's start
    node to its goal node, respecting node and connection capacity
    limits, following the routes described by a Solution.Path tree.

    Attributes:
        drones (list[Simulation.Drone]): All drones in the simulation.
        n_drones (int): Total number of drones being simulated.
        graph (Graph): Graph the simulation runs on.
    """

    class Drone:
        """A single drone moving through the graph.

        Attributes:
            location (Solution.Path.PathNode): Drone's current position
                in the path tree.
            visited (list[Solution.Path.PathNode]): History of path
                tree nodes this drone has occupied.
            number (int): Identifier of this drone.
        """

        location: Solution.Path.PathNode

        def __init__(self, number: int) -> None:
            """Initializes a drone.

            Args:
                number (int): Identifier of this drone.
            """
            self.visited: list[Solution.Path.PathNode] = []
            self.number: int = number

        def move(self, dest: Solution.Path.PathNode) -> None:
            """Moves the drone to a new path tree node.

            Records the current location in the visit history,
            increments the traversed connection's pass-through counter
            when moving between two graph nodes, and updates the
            drone's presence in the graph's node/connection drone
            lists.

            Args:
                dest (Solution.Path.PathNode): Path tree node to move
                    the drone to.
            """
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
        """Runs the full simulation from start to finish.

        Computes the minimum-weight path tree for the graph, creates
        `n_drones` drones at the start node, then repeatedly advances
        each drone one step along an available branch of the path tree
        (respecting node and connection capacity limits) until every
        drone has reached the goal node.

        Args:
            graph (Graph): Graph to simulate drone movement on.
            n_drones (int): Number of drones to simulate.

        Returns:
            list[list[Graph.Node | Graph.Connection]]: Per-drone
                sequence of nodes occupied at each simulation step,
                indexed by drone number.
        """
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
