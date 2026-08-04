from collections.abc import Callable
from typing import Optional as Opt


class ParsingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Parse:
    class Hub:
        def __init__(
            self,
            name: str,
            coords: tuple[int, int],
            metadata: dict[str, str | int],
            is_start: bool,
            is_goal: bool
        ) -> None:
            self.name: str = name
            self.x_pos, self.y_pos = coords
            self.is_start = False
            self.is_goal = False

            if 'zone' in metadata.keys():
                self.zone_type: str = metadata['zone']
            else:
                self.zone_type: str = 'normal'

            if is_start:
                self.is_start = True
            if is_goal:
                self.is_goal = True

    class Connection:
        def __init__(
            self,
            connection: str,
            metadata: dict[str, str | int]
        ):
            self.connection: str = connection
            if 'max_link_capacity' in metadata.keys():
                self.max_link_capacity: int = metadata['max_link_capacity']
            else:
                self.max_link_capacity: int = 1


    METADATA: tuple[str, str, str] = (
        'zone',
        'color',
        'max_link_capacity',
        'max_drones',
    )

    ZONES: tuple[str, str, str, str] = (
        'normal',
        'blocked',
        'restricted',
        'priority',
    )

    COLORS: tuple[str, str, str] = (
        'red',
        'green',
        'blue',
        'yellow',
        'gray'
    )

    @classmethod
    def main_parser(
        cls,
        file_name: str
    ) -> list[int, 'Parse.Hub', 'Parse.Connection']:
        FLAGS: dict[str, Callable[['Parse', str], str]] = {
            'nb_drones': cls.parse_nb_drones,
            'start_hub': cls.general_parse,
            'end_hub': cls.general_parse,
            'hub': cls.general_parse,
            'connection': cls.connection_parse
        }

        output: list[int, 'Parse.Hub', 'Parse.Connection'] = []

        line_nbr: int = 0
        i: int = 0
        with open(file_name, 'r') as file:
            for line in file:
                line_nbr += 1
                if line == '\n' or line[0] == '#':
                    continue
                if line_nbr == 1:
                    cls.parse_nb_drones(line)
                    continue
                raw_line: str = line
                line = line.strip().strip('\n')
                split_line:str = line.split(' ')
                split_line[0] = split_line[0].strip(':')

                line_is_valid: bool = cls.validate_line(line_nbr, raw_line)[0]
                err_msg: str = cls.validate_line(line_nbr, raw_line)[1]

                if not line_is_valid:
                    raise ParsingError(f'Invalid syntax in line {line_nbr}: {err_msg}')

                output.append(FLAGS[split_line[0]](line))
                i += 1

        return output

    @classmethod
    def parse_nb_drones(
        cls,
        line: str
    ) -> int:
        line = line.strip().strip('\n')
        line = line.split(' ')

        nbr_drones: int = int(line[1])

        return nbr_drones

    @classmethod
    def general_parse(
        cls,
        line: str
    ) -> 'Parse.Hub':
        line = line.strip().strip('\n')
        split_line: str = line.split(' ')
        metadata: dict[str, str | int] = {}
        name: str = split_line[1]
        is_start: bool = 'start_hub' in split_line[0]
        is_goal: bool = 'end_hub' in split_line[0]

        x, y = (split_line[2], split_line[3])

        if len(split_line) >= 5:
            metadata: dict[str, str | int] = cls.metadata_parse(' '.join(split_line[4:]))

        return cls.Hub(name, (x, y), metadata, is_start, is_goal)

    @classmethod
    def connection_parse(
        cls,
        line: str
    ) -> 'Parse.Connection':
        line = line.strip().strip('\n')
        split_line: list[str] = line.split(' ')
        metadata: dict[str, str | int] = {}

        if len(split_line) > 3 or len(split_line) < 2:
            raise ParsingError('1')
        
        names: str = split_line[1].split('-')
        if len(names) > 2:
            raise ParsingError('2')
        
        if len(split_line) >= 3:
            metadata = cls.metadata_parse(' '.join(split_line[2:]))
        
        return cls.Connection(split_line[1], metadata)

    @classmethod
    def metadata_parse(cls, raw_metadata: str) -> dict[str, str | int]:
        raw_metadata = raw_metadata.strip('[]')
        split_metadata: list[str] = raw_metadata.split(' ')
        metadata: dict[str, str | int] = {}

        for data in split_metadata:
            tag, value = data.split('=')

            if tag not in cls.METADATA:
                raise ParsingError('3')

            match tag:
                case 'zone':
                    #print(tag)
                    if value not in cls.ZONES:
                        raise ParsingError('4')
                    metadata[tag] = value
                case 'color':
                    if value not in cls.COLORS:
                        raise ParsingError('5')
                    metadata[tag] = value
                case 'max_drones':
                    if not value.isdigit():
                        raise ParsingError('6')
                    metadata[tag] = int(value)
                case 'max_link_capacity':
                    if not value.isdigit():
                        raise ParsingError('7')
                    metadata[tag] = int(value)

        return metadata

    @classmethod
    def validate_line(cls, line_nbr: int, raw_line: str) -> tuple[bool, str]:
        split_line: list[str] = raw_line.split(' ')
        metadata_start: int = 0
        count: int = 0
        for thing in split_line:
            if '[' in thing:
                metadata_start = count
                break
            count += 1

        metadata: str = raw_line.split(' ')[metadata_start]
        for thing in split_line[metadata_start:]:
            metadata += ' ' + thing

        if metadata_start != 0 and not (metadata[0] == '[' and metadata[-2] == ']'):
            print(metadata, metadata[-2])
            return (False, 'Metadata needs to be enclosed in brackets "[]"')
        return (True, '')
