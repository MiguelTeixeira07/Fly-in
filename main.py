from parsing import Parse, ParsingError
from graph import Graph
from solution import Solution


def main() -> None:
    try:
        data: list[int | 'Parse.Hub' | 'Parse.Connection'] = Parse.main_parser('config.txt')
    except ParsingError as e:
        print(e)
        return

    names: list[str] = []
    zone_types: list[str] = []
    connections: list[str] = []

    for element in data[0:]:
        if isinstance(element, Parse.Hub):
            names.append(element.name)
            zone_types.append(element.zone_type)
            if element.is_start:
                start: str = element.name
            if element.is_goal:
                goal: str = element.name
        if isinstance(element, Parse.Connection):
            connections.append(element.connection)

    graph = Graph(names, zone_types, connections, start, goal)

    for node in graph.nodes:
        print(node.name, '-', node.weight)
        if node.connections:
            print(' | '.join([n.name for n in node.connections]), end='\n\n')

    solution: list[Graph.Node] = Solution.shortest_path(graph)

    print('\nsolution:')
    for node in solution:
        print(node.name, end=' ')
    print(f'| Total weight: {Solution.get_weight_sum(solution)}')


if __name__ == '__main__':
    main()
