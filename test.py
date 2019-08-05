from level import *

init_screen = ScreenNumber(0)
buttons = [AddSubButton(2), AddSubButton(3)]
goal = ScreenNumber(8)
max_moves = 3

level = Level(init_screen, buttons, goal, max_moves)
print(list(level.solve(solve_all=True)))