from level import *
from buttons import *

init_screen = ScreenNumber(1)
buttons = [
    MemButton()
]
goal = ScreenNumber(1111)
max_moves = 4

level = Level(init_screen, buttons, goal, max_moves)
print(list(level.solve(solve_all = True, debug = True)))