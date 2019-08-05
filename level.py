from buttons import *
from screen import *
from typing import List, Set
from itertools import product, chain

import copy

class Level:
    init_screen: Screen = None
    init_buttons: Set[Button] = set()

    screen: Screen = None
    buttons: Set[Button] = set()
    goal: ScreenNumber = None
    max_moves: int = 0

    def __init__(self, init_number: ScreenNumber, buttons: Set[Button], goal: ScreenNumber, max_moves: int):
        assert init_number is not None
        assert buttons != set() and buttons is not None
        assert max_moves > 0

        # Store defaults
        self.init_screen = Screen(init_number)
        self.init_buttons = buttons # TODO: deep copy?

        # Copy defaults to game variables and initialize the rest
        self.screen = copy.deepcopy(self.init_screen)
        self.buttons = copy.deepcopy(self.init_buttons)
        self.goal = goal
        self.max_moves = max_moves

    def solve(self, solve_all = False, debug = False) -> List[List[Button]]:
        solutions = []
        # Iterate over all possible button combinations
        # TODO: self.init_buttons or self.buttons? self.buttons seems more appropriate, but we will modify the buttons we're iterating on.
        comb_lengths = [ product(self.buttons, repeat = l) for l in range(1, self.max_moves + 1) ]
        for combination in chain.from_iterable(comb_lengths):
            # Check if combination works
            # If it does, add it to the solutions list
            combination = list(combination)

            for button in combination:
                button.press(self.screen, self.buttons)
            
            if debug:
                print(f"Testing combination {combination}:")
                print(f"Result: {self.screen.screen_number.value}")

            if self.screen.screen_number is not None and self.screen.screen_number.value == self.goal.value:
                solutions.append(combination)
                if not solve_all:
                    return solutions

            # Reset buttons and screen
            self.screen = copy.deepcopy(self.init_screen)
            self.buttons = copy.deepcopy(self.init_buttons)

        return solutions
