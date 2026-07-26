from parsing import Parse, ParsingError


def main() -> None:
    try:
        data = Parse.main_parser('config.txt')
    except ParsingError as e:
        print(e)
    else:
        print(data)


if __name__ == '__main__':
    main()
