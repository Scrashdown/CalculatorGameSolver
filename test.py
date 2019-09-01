from solver import *
from buttons import *

init_screen = Screen(ScreenNumber(3002), portal_entrance=5, portal_exit=1)
buttons = [
    ConcButton(7),
    ReplaceButton('3', '5'),
    Inv10Button(),
    RSRButton()
]
goal = ScreenNumber(3507)
max_moves = 6

level = Solver(init_screen, buttons, goal, max_moves)
print("Computing solutions...")
solutions = list(level.solve(solve_all = True, debug = False))
print(f"Result:\n    {solutions}")