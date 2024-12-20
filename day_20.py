from common import *
from heapq import heappush, heappop
from dataclasses import dataclass, field
from typing import Any
from sys import maxsize
from math import comb

def parse_grid(lines):
    grid = []
    for row, l in enumerate(lines):
        grid.append(list())
        for col, c in enumerate(l):
            grid[-1].append(c)
            if c == "S":
                start = (row, col)
            elif c == "E":
                end = (row, col)
    return grid, start, end

@dataclass(order=True)
class QueueEntry:
    weight: int
    item: Any = field(compare=False)

class PriorityQueue:
    def __init__(self):
        self.q = []
        self.items = {}

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def push(self, item, weight):
        entry = QueueEntry(weight, item)
        self.items[item] = entry
        heappush(self.q, entry)

    def pop(self):
        while self.q:
            entry = heappop(self.q)
            item = entry.item
            if item is not None:
                del self.items[item]
                return entry.item, entry.weight
        raise KeyError("Empty queue")

    def get_weight(self, item):
        return self.items[item].weight

    def set_weight(self, item, new_weight):
        entry = self.items.pop(item)
        entry.item = None
        self.push(item, new_weight)

def get_next_nodes(row, col, grid, h, w):
    next = []
    for d in range(4):
        nr, nc = row + D.dy[d], col + D.dx[d]
        if bounds([nr, nc], [(0, h), (0, w)]):
            if grid[nr][nc] != "#":
                next.append((nr, nc))
    return next

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, end):
    h, w = len(grid), len(grid[0])

    gscore = defaultdict(lambda: maxsize)
    gscore[start] = 0

    open = PriorityQueue()
    open.push(start, manhattan(start, end))
    prev = dict()

    while len(open):
        current, _ = open.pop()
        row, col = current
        if current == end:
            return gscore, prev
        
        for next in get_next_nodes(row, col, grid, h, w):
            gtent = gscore[current] + 1
            if gtent < gscore[next]:
                prev[next] = current
                gscore[next] = gtent
                fscore = gtent + manhattan(current, next)
                if next not in open:
                    open.push(next, fscore)
                else:
                    open.set_weight(next, fscore)
    return None

def find_path(dist, prev, start, end):
    pos = end
    path = [end]
    while pos != start:
        pos = prev[pos]
        path.append(pos)
    return list(reversed(path)), dist[end] - dist[start]

def day20_part1(filename, threshold):
    lines = parse_lines(filename)
    grid, start, end = parse_grid(lines)
    h, w = len(grid), len(grid[0])

    dist, prev = astar(grid, start, end)
    nocheat_path, nocheat_length = find_path(dist, prev, start, end)
    nocheat_path = set(nocheat_path)

    cheats = []
    for row in range(h):
        for col in range(w):
            if bounds([row, col], [(1, h-1), (1, w-1)]):
                if grid[row-1][col] != "#" and grid[row][col] == "#" and grid[row+1][col] != "#":
                    cheats.append([(row-1, col), (row+1, col)])
                if grid[row][col-1] != "#" and grid[row][col] == "#" and grid[row][col+1] != "#":
                    cheats.append([(row, col-1), (row, col+1)])
    
    nshort = 0
    for (cheat_start, cheat_end) in cheats:
        d = 2
        if dist[cheat_start] > dist[cheat_end]:
            cheat_start, cheat_end = cheat_end, cheat_start
        assert cheat_start in dist
        assert cheat_end in dist
        d = 2 + dist[cheat_start] + (dist[end] - dist[cheat_end])
        if d <= nocheat_length - threshold:
            nshort += 1
    return nshort

def day20_part2(filename, threshold):
    lines = parse_lines(filename)
    grid, start, end = parse_grid(lines)

    dist, prev = astar(grid, start, end)
    nocheat_path, nocheat_length = find_path(dist, prev, start, end)

    nshort = 0
    for cheat_start, cheat_end in tqdm(it.combinations(nocheat_path, 2), desc="Trying all cheats", total=comb(len(nocheat_path), 2), leave=False):
        cheat_length = manhattan(cheat_start, cheat_end)
        if cheat_length > 20:
            continue
        if dist[cheat_start] > dist[cheat_end]:
            cheat_start, cheat_end = cheat_end, cheat_start
        d = cheat_length + dist[cheat_start] + (dist[end] - dist[cheat_end])
        if d <= nocheat_length - threshold:
            nshort += 1
    return nshort

if __name__ == "__main__":
    print("Part 1 example", day20_part1("input/day20_example.txt", 0))
    print("Part 1", day20_part1("input/day20.txt", 100))
    print("Part 2 example", day20_part2("input/day20_example.txt", 50))
    print("Part 2", day20_part2("input/day20.txt", 100))
