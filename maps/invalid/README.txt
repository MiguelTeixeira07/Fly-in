Parser invalid-input test corpus

Each file is intended to isolate one malformed input or semantic edge case.
Comments beginning with # and empty lines are included in a few tests because
they should normally be ignored according to the parser format.

The tests assume the syntax shown in the supplied example:
  nb_drones: N
  start_hub: NAME X Y [metadata]
  hub: NAME X Y [metadata]
  end_hub: NAME X Y [metadata]
  connection: NAME-NAME [metadata]

Some tests depend on semantic rules that may differ from your implementation
(e.g. whether duplicate connections, duplicate coordinates, unreachable goals,
or capacities greater than nb_drones are forbidden).

If you send me your parser.py / parsing.py, I can make a second corpus that is
specifically exhaustive against YOUR actual validation rules, including tests
for every branch and every expected ParsingError.
