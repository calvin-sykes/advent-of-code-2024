import itertools as it
from collections import Counter, defaultdict, deque
from tqdm.auto import tqdm, trange

class D:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    directions = "<^>v"
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]

def parse_lines(filename):
    """Read file and return lines split by carriage returns"""
    with open(filename, "r") as f:
        lines = f.readlines()
    return [l.rstrip("\n") for l in lines if l.strip()]

def bounds(vars, bounds):
    """
    For each in vars, check if it lies between corresponding pair of bounds.
    If a single bound is passed, it will apply to all vars.
    Returns true iff all vars are within bounds.
    """
    if len(bounds) == 1 and len(bounds[0]) == 2:
        bounds = it.repeat(bounds)

    for v, b in zip(vars, bounds):
        if v < b[0] or v >= b[1]:
            return False
    return True

def plot_grid(grid):
    print("\n".join(["".join(l) for l in grid]))