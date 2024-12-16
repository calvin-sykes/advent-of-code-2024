from common import *
from heapq import heappush, heappop
from dataclasses import dataclass, field
from typing import Any
from sys import maxsize

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

def get_next_nodes(row, col, facing):
    return [((row + D.dy[facing], col + D.dx[facing]), facing),
            ((row, col), (facing - 1) % 4),
            ((row, col), (facing + 1) % 4)]

def get_prev_nodes(row, col, facing):
    return [((row - D.dy[facing], col - D.dx[facing]), facing),
            ((row, col), (facing + 1) % 4),
            ((row, col), (facing - 1) % 4)]

def dijkstra(grid, start):    
    prev = dict()
    prev[(start, D.RIGHT)] = None
    dist = defaultdict(lambda: maxsize)
    dist[(start, D.RIGHT)] = 0
    nodes = PriorityQueue()
    nodes.push((start, D.RIGHT), 0)
    
    while nodes:
        ((row, col), facing), dist_so_far = nodes.pop()
        next_nodes = get_next_nodes(row, col, facing)
        for (next, cost) in zip(next_nodes, [1, 1000, 1000]):
            (nr, nc), _ = next
            if grid[nr][nc] != "#":
                dist_step = dist_so_far + cost
                if dist_step <= dist[next]:
                    dist[next] = dist_step
                    prev[next] = (row, col), facing
                    if next not in nodes:
                        nodes.push(next, dist[next])
                    else:
                        nodes.set_weight(next, dist[next])
    return dist, prev

def find_path(dist, prev, end):
    for pos in prev:
        if pos[0] == end:
            break
    else:
        raise ValueError
    length = dist[pos]

    path = []
    while pos:
        path.append(pos)
        pos = prev[pos]
    return path, length

def find_all_paths(dist, prev, end, best_length):
    saved_paths = []

    def traverse(dist, prev, start, path):
        if prev[start] is None:
            saved_paths.append(path.copy())
            return
        (row, col), facing = start
        parent = prev[start]
        best_dist = dist[parent]
        for prev_node in get_prev_nodes(row, col, facing):
            if dist[prev_node] <= best_dist:
                path.append(prev_node)
                traverse(dist, prev, prev_node, path)
                path.remove(prev_node)
    
    for d in range(4):
        if (end, d) in prev and dist[(end, d)] == best_length:
            traverse(dist, prev, (end, d), [(end, d)])
    return saved_paths

def day16_part1(filename):
    lines = parse_lines(filename)
    grid, start, end = parse_grid(lines)
    
    dist, prev = dijkstra(grid, start)
    _, length = find_path(dist, prev, end)
    return length

def day16_part2(filename):
    lines = parse_lines(filename)
    grid, start, end = parse_grid(lines)
    
    dist, prev = dijkstra(grid, start)
    _, length = find_path(dist, prev, end)
    paths = find_all_paths(dist, prev, end, length)
    
    seen = set()
    for p in paths:
        for (r, c), _ in p:
            seen.add((r, c))
    return len(seen)

if __name__ == "__main__":
    print("Part 1 example", day16_part1("input/day16_example.txt"))
    print("Part 1 example 2", day16_part1("input/day16_example2.txt"))
    print("Part 1", day16_part1("input/day16.txt"))
    print("Part 2 example", day16_part2("input/day16_example.txt"))
    print("Part 2 example 2", day16_part2("input/day16_example2.txt"))
    print("Part 2", day16_part2("input/day16.txt"))
