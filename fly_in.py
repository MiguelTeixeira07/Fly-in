import sys
from typing import Union


class Fly_In:
    """Application launcher for the Fly-In drone routing program.

    Groups the command-line entry point as a static method so the module
    can be imported elsewhere without triggering execution.
    """

    @staticmethod
    def main() -> None:
        """Runs the Fly-In application.

        Reads the map file path from the command line, parses it into
        hubs and connections, builds a graph from the parsed data,
        checks that the graph is fully connected, and starts the GUI.

        Expected usage:
            python3 fly_in.py <path/to/map>

        Args:
            None: Arguments are read directly from sys.argv.

        Returns:
            None

        Raises:
            None: Invalid arguments, parsing errors, and disconnected
                graphs are handled internally and reported by printing
                a message instead of raising an exception.
        """
        if len(sys.argv) != 2:
            print('Invalid arguments')
            print('Expected usage: python3 fly_in.py <path/to/map>')
            return

        from parsing import Parse, ParsingError

        try:
            data: list[Union[int, 'Parse.Hub', 'Parse.Connection']] = \
                Parse.main_parser(
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
            print('No possible path from start to end')
            return

        from gui import Gui

        if isinstance(data[0], int):
            Gui.run(graph, data[0])


if __name__ == '__main__':
    try:
        Fly_In.main()
    except KeyboardInterrupt:
        sys.exit(0)
