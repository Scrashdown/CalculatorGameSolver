from buttons import *
from screen import *
from typing import List, Set

class Level:
    screen: Screen = None
    buttons: Set[Button] = set()
    goal: ScreenNumber = None
    max_moves: int = 0

    def __init__(self, init_number: ScreenNumber, buttons: Set[Button], goal: ScreenNumber, max_moves: int):
        assert init_number is not None
        assert buttons != set()
        assert max_moves > 0

        # Initialize screen with initial number
        self.screen = Screen(init_number)
        # Initialize the rest
        self.buttons = buttons
        self.goal = goal
        self.max_moves = max_moves

    def solve(self) -> List[Button]:
        # TODO, use itertools
        pass