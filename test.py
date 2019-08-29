from level import *
from buttons import *

init_screen = ScreenNumber(369)
buttons = [
    ReplaceButton('93', '63'),
    ReplaceButton('63', '33'),
    ReplaceButton('36', '93'),
    Inv10Button(),
    ReplaceButton('39', '33')
]
goal = ScreenNumber(777)
max_moves = 5

level = Level(init_screen, buttons, goal, max_moves)
print("Computing solutions...")
solutions = list(level.solve(solve_all = True, debug = False))
print(f"Result:\n    {solutions}")