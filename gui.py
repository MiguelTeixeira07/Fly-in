import pygame
from typing import Optional as Opt
from time import sleep
from graph import Graph


class Gui:
    width: int = 900
    height: int = 600

    @classmethod
    def __init__(cls, graph) -> None:
        cls.running: bool = True
        cls.scale: list[int, int] = Gui.get_scale(graph)
        if cls.scale[0] == 0:
            cls.scale[0] = 1
        if cls.scale[1] == 0:
            cls.scale[1] = 1

    @classmethod
    def run(
        cls,
        graph: Graph,
    ) -> None:
        from simulation import Simulation

        sim_output: dict[int, list[Graph.Node]] = Simulation.start()

        pygame.init()

        cls.screen = pygame.display.set_mode((1200, 800))


        pygame.display.flip()

        index = 0

        while cls.running:
            cls.screen.fill((50, 50, 50))
            Gui.draw_graph(graph, sim_output, index)
            index += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cls.running = False
                    break
            sleep(1)

        pygame.quit()
        exit(0)

    @classmethod
    def draw_graph(cls, graph: Graph, sim_output: list[list[Graph.Node]], turn: int) -> None:
        if turn >= len(sim_output[0]):
            return
        print('\nturn', turn, '\n')

        for node in graph.nodes:
            x1, y1 = node.pos
            x1 = (cls.width / cls.scale[0]) * x1 / 2 + 25
            y1 = (cls.height / cls.scale[1]) * y1 / 2 + 500
            for con in node.connections:
                x2, y2 = con[0].pos
                x2 = (cls.width / cls.scale[0]) * x2 / 2 + 25
                y2 = (cls.height / cls.scale[1]) * y2 / 2 + 500
                pygame.draw.line(cls.screen, (200, 200, 200), (x1, y1), (x2, y2), 3)

        for node in graph.nodes:
            x, y = node.pos
            x = (cls.width / cls.scale[0]) * x / 2 + 25
            y = (cls.height / cls.scale[1]) * y / 2 + 500
            pygame.draw.circle(cls.screen, (255, 125, 0), (x, y), 15)
            for drone in sim_output:
                if drone[turn] == node:
                    print(f'drone{sim_output.index(drone)} in node {node.name}')
                    pygame.draw.circle(cls.screen, (30*sim_output.index(drone), 10*sim_output.index(drone), 10*sim_output.index(drone)), (x, y), 30)

        pygame.display.flip()

    @classmethod
    def close(cls) -> None:
        cls.running = False

    def get_scale(graph: Graph) -> list[int, int]:
        delta_x: int = 0
        delta_y: int = 0
        max_x: int = 0
        max_y: int = 0
        min_x: int = graph.nodes[0].pos[0]
        min_y: int = graph.nodes[0].pos[1]

        for node in graph.nodes:
            if node.pos[0] > max_x:
                max_x = node.pos[0]
            if node.pos[1] > max_x:
                max_y = node.pos[0]

            if node.pos[0] < max_x:
                min_x = node.pos[0]
            if node.pos[1] < max_y:
                min_y = node.pos[0]

        delta_x = max_x - min_x
        delta_y = max_y - min_y

        return [delta_x, delta_y]
