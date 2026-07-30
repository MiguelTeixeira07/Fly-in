from parsing import Parse, ParsingError
from graph import Graph


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
        if isinstance(element, Parse.Connection):
            connections.append(element.connection)

    graph = Graph(names, zone_types, connections)

    for node in graph.nodes:
        print(node.name)
        if node.connections:
            print(node.connections[0].name, node.connections[1].name, sep='-', end='\n\n')


if __name__ == '__main__':
    main()
