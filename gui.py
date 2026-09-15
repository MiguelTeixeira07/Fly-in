import pygame
import time
from typing import Any
from graph import Graph


class Gui:
    screen: Any

    @classmethod
    def run(
        cls,
        graph: Graph,
        n_drones: int
    ) -> None:
        from simulation import Simulation

        sim_output: list[
            list[
                Graph.Node | Graph.Connection
            ]
        ] = Simulation.start(graph, n_drones)

        pygame.init()

        cls.screen = pygame.display.set_mode((1200, 800))

        pygame.display.flip()

        index = 0

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
        sim_output: list[list[Graph.Node | Graph.Connection]],
        turn: int
    ) -> None:
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
                pygame.draw.circle(cls.screen, (255, 125, 0), (x, y), 15)

            for drone in sim_output:
                if drone[turn] == object:
                    pygame.draw.circle(
                        cls.screen,
                        (
                            10*sim_output.index(drone),
                            0*sim_output.index(drone),
                            0*sim_output.index(drone)
                        ),
                        (x, y),
                        10
                    )
                    print(drone[turn].name, object.name)

        for drone in sim_output:
            if drone[turn] != graph.start and drone[turn] != drone[turn - 1]:
                print(f'D{sim_output.index(drone) + 1}'
                      f'-{drone[turn].name}', end=' ')

        pygame.display.flip()

    @staticmethod
    def get_scale(graph: Graph) -> list[int]:
        max_x, max_y = graph.nodes[0].pos

        for node in graph.nodes:
            if node.pos[0] > max_x:
                max_x = node.pos[0]
            if node.pos[1] > max_y:
                max_y = node.pos[1]

        return [max_x + 1, max_y + 1]
