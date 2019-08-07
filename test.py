from level import *

init_screen = ScreenNumber(10)
buttons = [
    AddSubButton(2),
    IncrementButtonsButton(1)
]
goal = ScreenNumber(15)
max_moves = 3

level = Level(init_screen, buttons, goal, max_moves)
print(list(level.solve(solve_all = True)))