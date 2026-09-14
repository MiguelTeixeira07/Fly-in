import sys


def main() -> None:
    if len(sys.argv) != 2:
        print('Invalid arguments')
        print('Expected usage: python3 fly_in.py <path/to/map>')
        return

    from parsing import Parse, ParsingError

    try:
        data: list[int | Parse.Hub | Parse.Connection] = Parse.main_parser(
            sys.argv[1]
        )
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
            positions.append((element.x_pos, element.y_pos))
            if element.is_start:
                start: str = element.name
                if isinstance(data[0], int):
                    max_drones[-1] = data[0]
            if element.is_goal:
                goal: str = element.name
                if isinstance(data[0], int):
                    max_drones[-1] = data[0]
        if isinstance(element, Parse.Connection):
            connections.append((element.name, element.max_link_capacity))

    from graph import Graph

    graph = Graph(
        names,
        zone_types,
        connections,
        start,
        goal,
        positions,
        max_drones
    )

    if not Graph.graph_is_connected(graph):
        print('Map contains isolated hubs')
        return

    from gui import Gui

    if isinstance(data[0], int):
        Gui.run(graph, data[0])


if __name__ == '__main__':
    main()
