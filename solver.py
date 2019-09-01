from level import *

class Solver:
    def __call__(self, level: Level, solve_all = False, debug = False) -> List[List[Button.Action]]:
        return self.solve(level, solve_all = solve_all, debug = debug)

    def solve(self, level: Level, solve_all = False, debug = False) -> List[List[Button.Action]]:
        solutions: List[List[Button.Action]] = []

        # Idea: for each combination, use list of pairs of indexes (*, *) instead of list of actions
        # Then, for each combination, deepcopy the used buttons, and use (nb, na)
        # where nb = # of button, na = # of action within button nb to retrieve actions
        # from copied button list => for each combination, deepcopy (used) buttons

        # Create index of buttons and actions
        buttons_idxs = range(len(level.buttons))
        buttons_actions_idxs = [ (bi, ai) for bi in buttons_idxs for ai in range(len(level.buttons[bi].actions)) ]

        # Compute number of iterations without unrolling the iterator
        num_combinations = sum([ len(buttons_actions_idxs) ** i for i in range(1, level.max_moves + 1) ])
        percentage_reached = 0

        # Iterate over all possible combinations of actions
        comb_by_len = [ product(buttons_actions_idxs, repeat = l) for l in range(1, level.max_moves + 1) ]
        all_combinations = chain.from_iterable(comb_by_len)
        for (i, combination) in enumerate(all_combinations):
            # Display progress
            percentage = 100 * i / num_combinations
            if percentage > percentage_reached:
                print(f"{int(percentage_reached)}%", end = '\r')
                percentage_reached += 1

            # Deepcopy all used buttons, works because one action cannot be bound to several buttons
            copied_buttons = copy.deepcopy(level.buttons)

            # Retrieve actions from copied buttons
            copied_actions = [ copied_buttons[bi].actions[ai] for (bi, ai) in combination ]

            if debug:
                print(f"Testing combination {copied_actions}")

            # Execute actions and build tentative solution
            tentative_sol: List[Button.Action] = []
            for action in copied_actions:
                tentative_sol.append(copy.deepcopy(action))
                action(level.screen, copied_buttons)

                if debug:
                    print(f"    action: {action}")
                    print(f"    buttons: {copied_buttons}")
                    print(f"    screen: {level.screen.screen_number.value}")
                    print()

            if debug:
                print(f"Result: {level.screen.screen_number.value}")
                print(f"Goal: {level.goal.value}, (reached: {level.screen.screen_number.value == level.goal.value})")
                print()

            if level.screen.screen_number is not None and level.screen.screen_number.value == level.goal.value:
                # Shallow copy tentative solution so we can clear it later without deleting it from the solution
                solutions.append(copy.copy(tentative_sol))
                if not solve_all:
                    level.screen = copy.deepcopy(level.init_screen)
                    return solutions

            # Reset screen
            level.screen = copy.deepcopy(level.init_screen)

        return solutions
