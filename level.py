from buttons import Button
from screen import Screen, ScreenNumber
from typing import List, Set
from itertools import product, chain

import copy


class Level:
    init_screen: Screen = None

    screen: Screen = None
    buttons: List[Button] = []
    goal: ScreenNumber = None
    max_moves: int = 0

    repr_format = "Level(\n    init_screen = {},\n    init_buttons = {},\n    goal = {},\n    max_moves = {}\n)"

    def __init__(self, screen: Screen, buttons: List[Button],
                 goal: ScreenNumber, max_moves: int):
        assert screen is not None
        assert buttons != set() and buttons is not None
        assert max_moves > 0

        # Store defaults
        self.init_screen = screen

        # Copy defaults to game variables and initialize the rest
        self.screen = copy.deepcopy(self.init_screen)
        self.buttons = buttons
        self.goal = goal
        self.max_moves = max_moves

    def __repr__(self) -> str:
        return self.repr_format.format(self.init_screen, self.buttons, self.goal, self.max_moves)
