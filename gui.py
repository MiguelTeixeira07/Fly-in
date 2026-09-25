import pygame
import time
from typing import Any
from collections.abc import Callable
from graph import Graph
from enum import Enum




class Gui:
    """Pygame-based visualization of a drone routing simulation.

    Runs the simulation to completion, then renders each simulation
    step to a window, drawing the graph's nodes, connections, and
    drone positions over time.

    Attributes:
        screen (Any): Active pygame display surface.
        COLORS (dict[str, tuple[int, int, int]]): List of colors
    """

    screen: Any

    COLORS: dict[str, tuple[int, int, int]] = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "gray": (127, 127, 127),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "purple": (255, 0, 255),
        "cyan": (0, 255, 255),
        "orange": (255, 165, 0),
        "brown": (150, 75, 0),
        "maroon": (85, 0, 0),
        "darkred": (140, 0, 0),
        "violet": (127, 0, 255),
        "crimson": (178, 34, 34),
        "gold": (239, 192, 4),
        "default": (255, 255, 255)
    }

    DEFAULT_COLOR: tuple[int, int, int] = (255, 255, 255)

    @classmethod
    def run(
        cls,
        graph: Graph,
        n_drones: int
    ) -> None:
        """Runs the simulation and displays it in a pygame window.

        Computes the full simulation output ahead of time, then opens a
        window and advances one simulation step per second, drawing the
        graph and drone positions on each step, until the window is
        closed.

        Args:
            graph (Graph): Graph to simulate and display.
            n_drones (int): Number of drones to simulate.

        Returns:
            None

        Side Effects:
            Opens and eventually closes a pygame window, and terminates
            the process via `exit(0)` once the window is closed.
        """
        from simulation import Simulation

        sim_output: list[
            list[
                int | Graph.Node | Graph.Connection
            ]
        ] = Simulation.start(graph, n_drones)

        pygame.init()

        cls.screen = pygame.display.set_mode((1200, 800))

        pygame.display.flip()

        index = 1

        running: bool = True
        current_time: int = 0
        while running:
            cls.screen.fill((50, 50, 50))
            if index < len(sim_output[0]) and int(time.time()) != current_time:
                Gui.draw_graph(graph, sim_output, index)
                print()
                current_time = int(time.time())
                index += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

        pygame.quit()
        exit(0)

    @classmethod
    def draw_graph(
        cls,
        graph: Graph,
        sim_output: list[list[int | Graph.Node | Graph.Connection]],
        turn: int
    ) -> None:
        """Draws the graph and drone positions for a single simulation step.

        Scales node positions to fit the window, draws connection lines
        between adjacent nodes, draws a circle for each node, and draws
        a smaller circle for each drone at its current position on the
        given turn.

        Args:
            graph (Graph): Graph being visualized.
            sim_output (list[list[Graph.Node | Graph.Connection]]): Per
                -drone sequence of visited nodes/connections across the
                whole simulation.
            turn (int): Index of the simulation step to draw.

        Returns:
            None

        Side Effects:
            Draws to `cls.screen` and flips the pygame display. Prints
            drone movement information to stdout. Does nothing if
            `turn` is out of range.
        """
        if turn >= len(sim_output[0]):
            return

        scale = Gui.get_scale(graph)

        if scale[0] <= 0:
            scale[0] = 1
        if scale[1] <= 0:
            scale[1] = 1

        for object in graph.nodes + graph.connections:
            x_pos, y_pos = object.pos
            x1 = (1200 / scale[0]) * x_pos + 1200 / (scale[0] * 2)
            y1 = (800 / scale[1]) * y_pos + 800 / (scale[1] * 2)

            if isinstance(object, Graph.Connection):
                continue

            for con in object.connections:
                x_pos, y_pos = con.get_opposite_node(object).pos
                x2 = (1200 / scale[0]) * x_pos + 1200 / (scale[0] * 2)
                y2 = (800 / scale[1]) * y_pos + 800 / (scale[1] * 2)
                pygame.draw.line(
                    cls.screen,
                    (200, 200, 200),
                    (x1, y1),
                    (x2, y2),
                    3
                )

        for object in graph.nodes + graph.connections:
            x_pos, y_pos = object.pos
            x = (1200 / scale[0]) * x_pos + 1200 / (scale[0] * 2)
            y = (800 / scale[1]) * y_pos + 800 / (scale[1] * 2)
            if isinstance(object, Graph.Node):
                pygame.draw.circle(
                    cls.screen,
                    cls.COLORS.get(object.color, cls.DEFAULT_COLOR),
                    (x, y),
                    15
                )

            for drone in sim_output:
                if drone[turn] == object:
                    pygame.draw.circle(
                        cls.screen,
                        (
                            int(255/len(sim_output)*sim_output.index(drone)),
                            0,
                            0
                        ),
                        (x, y),
                        10
                    )

        curr_pos: int | Graph.Node | Graph.Connection = sim_output[0][turn]
        for drone in sim_output:
            if drone[turn] != graph.start and curr_pos != drone[turn - 1]:
                print(f'D{sim_output.index(drone) + 1}', end='')
                if not isinstance(curr_pos, int):
                    print(f'-{curr_pos.name}', end=' ')

        pygame.display.flip()

    @staticmethod
    def get_scale(graph: Graph) -> list[int]:
        """Computes the coordinate scale needed to fit the graph on screen.

        Args:
            graph (Graph): Graph whose node positions determine the
                scale.

        Returns:
            list[int]: [x_scale, y_scale], one more than the maximum x
                and y coordinates among the graph's nodes.
        """
        max_x, max_y = graph.nodes[0].pos

        for node in graph.nodes:
            if node.pos[0] > max_x:
                max_x = node.pos[0]
            if node.pos[1] > max_y:
                max_y = node.pos[1]

        return [max_x + 1, max_y + 1]
