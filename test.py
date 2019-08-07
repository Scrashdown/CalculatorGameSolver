from level import *

init_screen = ScreenNumber(25)
buttons = [
    AddSubButton(8),
    MulButton(2),
    MulButton(5),
    IncrementButtonsButton(1)
]
goal = ScreenNumber(268)
max_moves = 5

level = Level(init_screen, buttons, goal, max_moves)
print(list(level.solve(solve_all = True)))