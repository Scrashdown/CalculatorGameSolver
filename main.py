import argparse

# Top-level parser
parser = argparse.ArgumentParser(description = 'Find solutions for Calculator: The Game')
subparsers = parser.add_subparsers()

## Parser reading level from command line
parser_cmd = subparsers.add_parser('cmd', help = 'Read one level description from command line arguments.')
parser_cmd.add_argument("init_num",
                        help = "the number displayed on the calculator when the game starts",
                        type = float) # TODO: Maybe change to int? If I switch the whole game to int.
parser_cmd.add_argument("max_moves",
                        help = "maximum allowed number of allowed moves",
                        type = int)
parser_cmd.add_argument("goal",
                        help = "goal of the level",
                        type = float) # TODO: Maybe change to int? If I switch the whole game to int.
parser_cmd.add_argument("buttons",
                        help = "list of buttons, separated by spaces, using the format described in the README",
                        type = str)
parser_cmd.add_argument("--portal",
                        help = "entrance and exit of the portal (starting at 1 from the RIGHT side of the screen), if any",
                        nargs = 2)


## Parser reading level(s) from a file
parser_file = subparsers.add_parser('file', help = 'Read one or several level descriptions from a given file.')
parser_file.add_argument("input_file",
                         help = "file containing level descriptions",
                         type = str)

parser.parse_args()
