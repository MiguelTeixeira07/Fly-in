from collections.abc import Callable
from typing import Optional as Opt, TextIO


class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
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
            self.zone_type: str = 'normal'
            self.max_drones: int = 1

            if 'zone' in metadata.keys():
                self.zone_type = str(metadata['zone'])
            if 'max_drones' in metadata.keys():
                self.max_drones = int(metadata['max_drones'])

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
            self.name: str = connection
            self.max_link_capacity: int = 1

            if 'max_link_capacity' in metadata.keys():
                self.max_link_capacity = int(metadata['max_link_capacity'])

    METADATA: tuple[str, str, str, str] = (
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

    @classmethod
    def main_parser(
        cls,
        file_name: str
    ) -> list[int | 'Parse.Hub' | 'Parse.Connection']:
        try:
            fd: TextIO = open(file_name, 'r')
        except PermissionError:
            raise ParsingError('Parsing Error: '
                               'Not enough permissions in map file')
        except FileNotFoundError:
            raise ParsingError('Parsing Error: '
                               f'File "{file_name}" was not found')
        else:
            fd.close()

        TAGS: dict[
            str,
            Callable[
                [str, int],
                int | 'Parse.Hub' | 'Parse.Connection'
            ]
        ] = {
            'nb_drones': lambda line, _: cls.parse_nb_drones(line),
            'start_hub': cls.general_parse,
            'end_hub': cls.general_parse,
            'hub': cls.general_parse,
            'connection': cls.connection_parse
        }
        output: list[int | 'Parse.Hub' | 'Parse.Connection'] = []

        line_nbr: int = 0
        i: int = 0
        with open(file_name, 'r') as file:
            for line in file:
                line_nbr += 1
                if line == '\n' or line[0] == '#':
                    continue

                raw_line: str = line
                line = line.strip().strip('\n')
                split_line: list[str] = line.split(' ')
                split_line[0] = split_line[0].strip(':')

                line_is_valid, err_msg = cls.validate_line(raw_line)

                if not line_is_valid:
                    raise ParsingError('Invalid syntax in line '
                                       f'{line_nbr}: {err_msg}')

                output.append(TAGS[split_line[0]](line, line_nbr))
                i += 1

        valid, err_msg = cls.check_output_validity(output)
        if not valid:
            raise ParsingError(f'Parsing Error: {err_msg}')

        return output

    @classmethod
    def parse_nb_drones(
        cls,
        line: str
    ) -> int:
        line = line.strip().strip('\n')

        return int(line.split()[1])

    @classmethod
    def general_parse(
        cls,
        line: str,
        line_nbr: int
    ) -> 'Parse.Hub':
        line = line.strip().strip('\n')
        split_line: list[str] = line.split(' ')
        metadata: dict[str, str | int] = {}
        name: str = split_line[1]
        is_start: bool = 'start_hub' in split_line[0]
        is_goal: bool = 'end_hub' in split_line[0]

        x, y = (int(split_line[2]), int(split_line[3]))

        if len(split_line) >= 5:
            metadata = cls.metadata_parse(
                ' '.join(split_line[4:]),
                line_nbr
            )

        return cls.Hub(name, (x, y), metadata, is_start, is_goal)

    @classmethod
    def connection_parse(
        cls,
        line: str,
        line_nbr: int
    ) -> 'Parse.Connection':
        line = line.strip().strip('\n')
        split_line: list[str] = line.split(' ')
        metadata: dict[str, str | int] = {}

        if len(split_line) >= 3:
            metadata = cls.metadata_parse(' '.join(split_line[2:]), line_nbr)

        return cls.Connection(split_line[1], metadata)

    @classmethod
    def metadata_parse(
        cls,
        raw_metadata: str,
        line_nbr: int
    ) -> dict[str, str | int]:
        valid: bool = False
        for item in raw_metadata.split():
            if any(char.isalnum() for char in item):
                valid = True
                break
        if not valid:
            raise ParsingError('Metadata is missing tokens')

        raw_metadata = raw_metadata.strip('[]')
        split_metadata: list[str] = raw_metadata.split(' ')
        metadata: dict[str, str | int] = {}

        repeat: bool = False
        for data in split_metadata:
            tag, value = data.split('=')

            if tag not in cls.METADATA:
                raise ParsingError('Invalid tag in metadata')

            if tag in metadata:
                raise ParsingError('Duplicated tag in metadata')

            match tag:
                case 'zone':
                    if value not in cls.ZONES:
                        print(f'Invalid syntax in line {line_nbr}:', end=' ')
                        raise ParsingError('Invalid zone')
                    metadata[tag] = value
                case 'max_drones':
                    if not value.isdigit():
                        print(f'Invalid syntax in line {line_nbr}:', end=' ')
                        raise ParsingError('Invalid ammount of drones')
                    metadata[tag] = int(value)
                    if int(metadata[tag]) <= 0:
                        print(f'Invalid syntax in line {line_nbr}:', end=' ')
                        raise ParsingError('Invalid ammount of drones')
                case 'max_link_capacity':
                    if not value.isdigit():
                        print(f'Invalid syntax in line {line_nbr}:', end=' ')
                        raise ParsingError('Invalid ammount of drones')
                    metadata[tag] = int(value)
                    if int(metadata[tag]) <= 0:
                        print(f'Invalid syntax in line {line_nbr}:', end=' ')
                        raise ParsingError('Invalid ammount of drones')
                case 'color':
                    if repeat:
                        print(f'Invalid syntax in line {line_nbr}:', end=' ')
                        raise ParsingError('Duplicated tag in metadata')
                    repeat = True
                    if not value.isalpha():
                        print(f'Invalid syntax in line {line_nbr}:', end=' ')
                        raise ParsingError('Invalid color')

        return metadata

    @staticmethod
    def validate_line(line: str) -> tuple[bool, str]:
        VALID_TAGS: dict[str, Callable[[str], tuple[bool, str]]] = {
            'nb_drones': Parse.validate_nb_drones,
            'start_hub': lambda line: Parse.validate_hub(
                line,
                start_end=True
            ),
            'end_hub': lambda line: Parse.validate_hub(line, start_end=True),
            'hub': Parse.validate_hub,
            'connection': Parse.validate_connection
        }
        if not line[0].isalpha():
            return (False, 'Invalid character in start of line')
        allowed_chars: str = ' -:[]_=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN'
        allowed_chars += 'OPQRSTUVWXYZ0123456789\n'
        test_line: str = line
        for char in allowed_chars:
            test_line = test_line.replace(char, '')
        if test_line != '':
            return (False, 'Forbidden character')

        tag: str = line.split()[0]

        if ':' not in line:
            return (False, 'Expected ":" after tag')

        if line.count(':') > 1:
            return (False, 'Invalid use of ":"')

        if tag.strip(':') not in VALID_TAGS:
            return (False, 'Invalid tag')

        valid, msg = Parse.validate_metadata(line)
        if not valid:
            return (valid, msg)

        valid, msg = VALID_TAGS[tag.strip(':')](line)

        return (valid, msg)

    @staticmethod
    def validate_nb_drones(line: str) -> tuple[bool, str]:
        if len(line.split()) != 2:
            return (False, f'Expected 1 token, got {len(line.split()) - 1}')

        if not line.split()[1].strip('-').isnumeric():
            return (False, 'Invalid token')

        if int(line.split()[1]) <= 0:
            return (False, 'Number of drones has to be positive')

        return (True, '')

    @staticmethod
    def validate_hub(line: str, start_end: bool = False) -> tuple[bool, str]:
        if len(line.split()) < 4:
            return (False, 'Hub requires at least 4 tokens')
        if len(line.split()) > 4 and '[' not in line.split()[4]:
            return (False, 'Too many tokens for Hub')

        if '-' in line.split()[1]:
            return (False, 'Hub name cannot contain "-"')

        if not (
            line.split()[2].strip('-').isnumeric() and
            line.split()[3].strip('-').isnumeric()
        ):
            return (False, 'Invalid coordinates')

        if start_end and 'max_drones' in line:
            return (
                False,
                'Start and end hubs must have unlimited drone capacity'
            )

        return (True, '')

    @staticmethod
    def validate_connection(line: str) -> tuple[bool, str]:
        if len(line.split()) < 2:
            return (False, 'Expected token after "Connection:"')

        if len(line.split()) > 2 and '[' not in line.split()[2]:
            return (False, 'Too many tokens for Connection')

        names: list[str] = line.split()[1].split('-')
        if len(names) > 2 or len(names) < 2:
            return (False, 'Invalid connection')

        if names[0] == names[1]:
            return (False, 'Invalid connection')

        return (True, '')

    @staticmethod
    def validate_metadata(line: str) -> tuple[bool, str]:
        index: int = 0
        metadata_start: Opt[int] = None
        for token in line.split():
            if '[' in token:
                metadata_start = index
            index += 1

        if not metadata_start:
            if ']' in line.split()[-1]:
                return (False, 'Unexpected "]"')
            else:
                return (True, '')

        if metadata_start and ']' not in line.split()[-1]:
            return (False, 'Expected "]" after "["')

        for token in line.split()[metadata_start:]:
            if token.count('=') != 1:
                return (False, 'Invalid use of "=" in metadata')

        return (True, '')

    @staticmethod
    def check_output_validity(
        output: list[int | 'Parse.Hub' | 'Parse.Connection']
    ) -> tuple[bool, str]:
        if not (
            any(type(item) is int for item in output)
            and any(isinstance(item, Parse.Hub) for item in output)
            and any(isinstance(item, Parse.Connection) for item in output)
        ):
            return (False, 'Impossible simulation')

        if not isinstance(output[0], int):
            return (False, 'Impossible simulation')

        coords: list[tuple[int, int]] = []
        hub_names: list[str] = []
        con_names: list[str] = []
        start_flag: bool = False
        end_flag: bool = False

        for item in output:
            if isinstance(item, Parse.Hub):
                if start_flag and item.is_start:
                    return (False, 'Map must contain only one start_hub')
                start_flag = item.is_start

                if end_flag and item.is_goal:
                    return (False, 'Map must contain only one end_hub')
                end_flag = item.is_goal

                if (item.x_pos, item.y_pos) in coords:
                    return (False, 'Coordinates must be unique to each hub')
                coords.append((item.x_pos, item.y_pos))

                if item.name in hub_names:
                    return (False, 'Name must be unique to each hub')
                hub_names.append(item.name)

            if isinstance(item, Parse.Connection):
                if (
                    item.name in con_names or
                    '-'.join(item.name.split('-')[::-1]) in con_names
                ):
                    return (False, 'Connections must not be repeated')
                con_names.append(item.name)

                if (
                    item.name.split('-')[0] not in hub_names or
                    item.name.split('-')[1] not in hub_names
                ):
                    return (
                        False,
                        'Connections must be between existing hubs'
                    )

        return (True, '')
