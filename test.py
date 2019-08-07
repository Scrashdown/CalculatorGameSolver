from level import *

init_screen = ScreenNumber(0)
buttons = [
    AddSubButton(-2),
    AddSubButton(5),
    MulButton(2),
    IncrementButtonsButton(1)
]
goal = ScreenNumber(42)
max_moves = 5

level = Level(init_screen, buttons, goal, max_moves)
print(list(level.solve(solve_all = True)))