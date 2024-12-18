from common import *
from heapq import heappush, heappop
from dataclasses import dataclass, field
from typing import Any
from sys import maxsize

def parse_bytes(lines):
    bytes = []
    for l in lines:
        bytes.append(tuple(map(int, l.split(","))))
    return bytes

def build_grid(bytes, h, w):
    grid = []
    for r in range(h):
        grid.append(list())
        for c in range(w):
            if (c, r) in bytes:
                grid[-1].append("#")
            else:
                grid[-1].append(".")
    return grid

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

def get_next_nodes(row, col, h, w):
    next = []
    for d in range(4):
        nr, nc = row + D.dy[d], col + D.dx[d]
        if bounds([nr, nc], [(0, h), (0, w)]):
            next.append((nr, nc))
    return next

def dijkstra(grid, start):
    h, w = len(grid), len(grid[0])
    prev = dict(); prev[start] = None
    dist = defaultdict(lambda: maxsize); dist[start] = 0
    nodes = PriorityQueue(); nodes.push(start, 0)
    
    while nodes:
        (row, col), dist_so_far = nodes.pop()
        for next in get_next_nodes(row, col, h, w):
            nr, nc = next
            if grid[nr][nc] != "#":
                dist_step = dist_so_far + 1
                if dist_step < dist[next]:
                    dist[next] = dist_step
                    prev[next] = (row, col)
                    if next not in nodes:
                        nodes.push(next, dist[next])
                    else:
                        nodes.set_weight(next, dist[next])
    return dist, prev

def find_path(dist, prev, end):
    for pos in prev:
        if pos == end:
            break
    else:
       return None, 0
    length = dist[pos]

    path = []
    while pos:
        path.append(pos)
        pos = prev[pos]
    return path, length

def day18_part1(filename, fieldsize, nbytes):
    lines = parse_lines(filename)
    h, w = fieldsize, fieldsize
    bytes = parse_bytes(lines)
    grid = build_grid(bytes[:nbytes], h, w)

    dist, prev = dijkstra(grid, (0, 0))
    _, length = find_path(dist, prev, (h-1, w-1))
    return length

def day18_part2(filename, fieldsize):
    lines = parse_lines(filename)
    h, w = fieldsize, fieldsize
    bytes = parse_bytes(lines)

    l, r = 0, len(bytes)
    while l <= r:
        nbytes = (l + r) // 2
        grid = build_grid(bytes[:nbytes+1], h, w)
        dist, prev = dijkstra(grid, (0, 0))
        path, _ = find_path(dist, prev, (h-1, w-1))
        if path is None:
            r = nbytes - 1
        else:
            l = nbytes + 1
    return ",".join(map(str, bytes[nbytes]))

if __name__ == "__main__":
    print("Part 1 example", day18_part1("input/day18_example.txt", 7, 12))
    print("Part 1", day18_part1("input/day18.txt", 71, 1024))
    print("Part 2 example", day18_part2("input/day18_example.txt", 7))
    print("Part 2", day18_part2("input/day18.txt", 71))
