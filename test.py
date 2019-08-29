from level import *
from buttons import *

init_screen = ScreenNumber(9)
buttons = [
    ReplaceButton("39", "93"),
    DivButton(3),
    MemButton(),
    ReplaceButton("31", "00")
]
goal = ScreenNumber(3001)
max_moves = 9

level = Level(init_screen, buttons, goal, max_moves)
print("Computing solutions...")
solutions = list(level.solve(solve_all = False, debug = False))
print(f"Result:\n    {solutions}")