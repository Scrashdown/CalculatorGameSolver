import argparse, re

from level import Level
from buttons import Button, button_regex
from screen import Screen, ScreenNumber
from typing import List, Tuple

class ButtonParser:
    def __init__(self):
        # Build dict linking compiled regex -> class
        # self.regex_constructor_matcher = { re.compile(r): cl for (cl, r) in button_regex.items() }
        self.regex_constructor_matcher = dict()
        for (cl, r) in button_regex.items():
            compiled = re.compile(r)
            self.regex_constructor_matcher[compiled] = cl

    def parse(self, button_list: str) -> List[Button]:
        '''Parse a string containing comma separated button representations and return the list of buttons.'''
        # Isolate buttons and remove optional spaces
        repr_list = map(lambda s: s.strip(), button_list.split(','))
        button_list = list(map(self.parse_button, repr_list))
        return button_list

    def parse_button(self, button: str) -> Button:
        '''Parse a single string representing a button.'''
        for r in self.regex_constructor_matcher:
            if r.fullmatch(button):
                class_ = self.regex_constructor_matcher[r]
                # Instantiate class using specialized static method because we cannot use the constructor
                # TODO: find a maybe better way to implement this
                return class_.instantiate(button)
        return None

class LevelParser:
    def __init__(self):
        # Top-level parser
        self.parser = argparse.ArgumentParser(description = 'Find solutions for Calculator: The Game')
        subparsers = self.parser.add_subparsers(title = "Subcommands")

        ## Parser reading level from command line
        self.cmd_parser = subparsers.add_parser('cmd', help = 'Read one level description from command line arguments.')
        self.cmd_parser.set_defaults(func = self.__parse_cmd)
        self.cmd_parser.add_argument("init_num",
                                help = "(float) the number displayed on the calculator when the game starts",
                                type = float) # TODO: Maybe change to int? If I switch the whole game to int.
        self.cmd_parser.add_argument("max_moves",
                                help = "(int > 0) maximum allowed number of allowed moves",
                                type = int)
        self.cmd_parser.add_argument("goal",
                                help = "(float) goal of the level",
                                type = float) # TODO: Maybe change to int? If I switch the whole game to int.
        self.cmd_parser.add_argument("buttons",
                                help = "list of buttons between "", separated by ',', using the format described in the README",
                                type = str)
        self.cmd_parser.add_argument("-p", "--portal",
                                help = "(int > 0) entrance and exit of the portal (starting at 1 from the RIGHT side of the screen), if any",
                                type = int, nargs = 2, metavar = ('in', 'out'))

        ## Parser reading level(s) from a file
        file_parser = subparsers.add_parser('file', help = 'Read one or several level descriptions from a given file.')
        file_parser.set_defaults(func = self.__parse_file)
        file_parser.add_argument("input_file",
                                help = "file containing level descriptions",
                                type = str)

        # Button parser
        self.button_parser = ButtonParser()

    def parse_args(self) -> List[Level]:
        '''Parse args from command line, either from file or command args, and return the list of levels.'''
        namespace = self.parser.parse_args()
        # Call suitable function depending on subcommand
        result = namespace.func(namespace)
        # Make sure result is enclosed in a list
        if type(result) is not list:
            return [result]
        return result

    def __parse_cmd(self, namespace) -> Level:
        screen = Screen(ScreenNumber(namespace.init_num), namespace.portal)
        # Parse buttons with specialized parser
        buttons = self.button_parser.parse(namespace.buttons)
        goal = ScreenNumber(namespace.goal)
        level = Level(screen, buttons, goal, namespace.max_moves)
        return level

    def __parse_file(self, namespace) -> List[Level]:
        with open(namespace.input_file) as input_file:
            levels = []
            for line in input_file:
                # Ignore comments
                if line.startswith('#'):
                    continue
                # Turn line into a list of arguments
                split = line.split("'")
                buttons: str = split[1]
                other_args_str = (split[0] + split[2]) if len(split) > 2 else split[0]
                other_args_raw = other_args_str.split(' ')
                other_args: List[str] = list(filter(lambda s: s != '', map(lambda s: s.strip(), other_args_raw)))
                args = other_args + [buttons]
                # Reuse command line parser (and thus command line syntax)
                line_namespace = self.cmd_parser.parse_args(args)
                new_level = self.__parse_cmd(line_namespace)
                levels.append(new_level)
            return levels
