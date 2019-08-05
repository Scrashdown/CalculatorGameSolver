from level import *

init_screen = ScreenNumber(128)
buttons = [
    MulButton(4),
    DivButton(4),
    SumButton(),
    ReplaceButton(5, 16)
]
goal = ScreenNumber(64)
max_moves = 4

level = Level(init_screen, buttons, goal, max_moves)
print(list(level.solve(solve_all=True)))