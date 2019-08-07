from buttons import *
from screen import *
from typing import List
from itertools import product, chain

import copy

class Level:
    init_screen: Screen = None
    init_buttons: List[Button] = []

    screen: Screen = None
    buttons: List[Button] = []
    goal: ScreenNumber = None
    max_moves: int = 0

    def __init__(self, init_number: ScreenNumber, buttons: List[Button], goal: ScreenNumber, max_moves: int):
        assert init_number is not None
        assert buttons != set() and buttons is not None
        assert max_moves > 0

        # Store defaults
        self.init_screen = Screen(init_number)

        # Copy defaults to game variables and initialize the rest
        self.screen = copy.deepcopy(self.init_screen)
        self.buttons = buttons
        self.goal = goal
        self.max_moves = max_moves

    def solve(self, solve_all = False, debug = False) -> List[List[Button]]:
        solutions: List[List[Button]] = []
        # Iterate over all possible button combinations
        comb_lengths = [ product(range(len(self.buttons)), repeat = l) for l in range(1, self.max_moves + 1) ]
        for combination in chain.from_iterable(comb_lengths):
            # Deep copy buttons using indexes from combination
            # Required because buttons may get modified
            tentative_solution: List[Button] = []
            button_combination = [ copy.deepcopy(self.buttons[idx]) for idx in combination ]

            for button in button_combination:
                # Deep copy button tokeep its current state in case it is updated later
                tentative_solution.append(copy.deepcopy(button))
                button.press(self.screen, button_combination)
            
            if debug:
                print(f"Testing combination {tentative_solution}:")
                print(f"Result: {self.screen.screen_number.value}")
                print(f"Goal: {self.goal.value}, (reached: {self.screen.screen_number.value == self.goal.value})")

            if self.screen.screen_number is not None and self.screen.screen_number.value == self.goal.value:
                # Shallow copy tentative solution so we can clear it later without deleting it from the solution
                solutions.append(copy.copy(tentative_solution))
                if not solve_all:
                    self.screen = copy.deepcopy(self.init_screen)
                    return solutions

            # Reset screen and tentative solution
            self.screen = copy.deepcopy(self.init_screen)
            tentative_solution.clear()

        return solutions
