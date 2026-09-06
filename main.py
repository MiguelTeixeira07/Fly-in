from parsing import Parse, ParsingError
from graph import Graph
from solution import Solution
from gui import Gui
from simulation import Simulation


def main() -> None:
    try:
        data: list[int | 'Parse.Hub' | 'Parse.Connection'] = Parse.main_parser('maps/custom/01_custom.txt')
    except ParsingError as e:
        print(e)
        return

    names: list[str] = []
    zone_types: list[str] = []
    max_drones: list[int] = []
    connections: list[tuple[str, int]] = []
    positions: list[tuple[int, int]] = []

    for element in data[0:]:
        if isinstance(element, Parse.Hub):
            names.append(element.name)
            zone_types.append(element.zone_type)
            max_drones.append(element.max_drones)
            print(element.max_drones)
            positions.append((element.x_pos, element.y_pos))
            if element.is_start:
                start: str = element.name
                max_drones[-1] = data[0]
            if element.is_goal:
                goal: str = element.name
                max_drones[-1] = data[0]
        if isinstance(element, Parse.Connection):
            connections.append((element.connection, element.max_link_capacity))

    print(names, zone_types, max_drones, positions, connections, sep='\n')

    graph = Graph(names, zone_types, connections, start, goal, positions, max_drones)

    for node in graph.nodes:
        print(node.name, '-', node.weight)
        if node.connections:
            print(' | '.join([n[0].name for n in node.connections]), end='\n\n')

    solution: list[Graph.Node] = Solution.path(graph)

    print('\nsolution:')
    for node in solution:
        print(node.name, end=' ')
    print(f'| Total weight: {Solution.get_weight_sum(solution)}')

    Simulation(graph, data[0])

    Gui(graph)
    Gui.run(graph)


if __name__ == '__main__':
    main()
