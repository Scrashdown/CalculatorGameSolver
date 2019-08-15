from buttons import Button
from screen import Screen, ScreenNumber
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

    def __init__(self, init_number: ScreenNumber, buttons: List[Button],
                 goal: ScreenNumber, max_moves: int):
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

    def solve(self, solve_all = False, debug = False) -> List[List[Button.Action]]:
        solutions: List[List[Button.Action]] = []

        # TODO: fix deepcopy hell and make sure references are correct

        # Get all actions from given buttons
        action_lists = [button.actions for button in self.buttons]
        actions = [item for sublist in action_lists for item in sublist]

        # Iterate over all possible *action* combinations
        comb_by_len = [product(actions, repeat = l)
                       for l in range(1, self.max_moves + 1)]
        all_combinations = chain.from_iterable(comb_by_len)
        for combination in all_combinations:
            tentative_sol: List[Button.Action] = []

            # Deep copy actions in a separate list, to keep their state at each moment,
            # should they get modified. This is done so the solutions appear consistent
            # to what is seen in the game. Buttons linked to the copied must be kept
            # in a list so they can be passed to the action() call.
            copied_combination = [copy.deepcopy(
                action) for action in combination]
            copied_buttons = list(
                set([action.button for action in copied_combination]))

            # TODO: error with deep copy. 2 actions that were originally linked to the same button,
            # are now linked to 2 duplicate, BUT SEPARATE, buttons, therefore the MEM Button doesn't work.

            for action in copied_combination:
                # Deep copy action to keep its current state, should it be modified later
                tentative_sol.append(copy.deepcopy(action))
                action(self.screen, copied_buttons)

            if debug:
                print(f"Testing combination {tentative_sol}:")
                print(f"Result: {self.screen.screen_number.value}")
                print(
                    f"Goal: {self.goal.value}, (reached: {self.screen.screen_number.value == self.goal.value})")

            if self.screen.screen_number is not None and self.screen.screen_number.value == self.goal.value:
                # Shallow copy tentative solution so we can clear it later without deleting it from the solution
                solutions.append(copy.copy(tentative_sol))
                if not solve_all:
                    self.screen = copy.deepcopy(self.init_screen)
                    return solutions

            # Reset screen
            self.screen = copy.deepcopy(self.init_screen)

        return solutions
