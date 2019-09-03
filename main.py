from parser import LevelParser
from solver import Solver

print("Parsing level...")
level_parser = LevelParser()
levels = level_parser.parse_args()

print("Solving...")
solver = Solver()
for (i, l) in enumerate(levels):
    print(f"    Level {i+1}:")
    solutions = solver.solve(l, solve_all=True)
    print(f"    Solution: {solutions}")