from common import *

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

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(grid, start, end):
    pos = start
    path = [start]
    prev = None
    while pos != end:
        for d in range(4):
            nr, nc = pos[0] + D.dy[d], pos[1] + D.dx[d]
            if grid[nr][nc] != "#" and (nr, nc) != prev:
                prev = pos
                pos = nr, nc
                path.append(pos)
                break
    return path, len(path)

def day20_part1(filename, threshold):
    lines = parse_lines(filename)
    grid, start, end = parse_grid(lines)
    h, w = len(grid), len(grid[0])

    nocheat_path, nocheat_length = find_path(grid, start, end)
    dist = dict(zip(nocheat_path, range(nocheat_length)))
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

    nocheat_path, nocheat_length = find_path(grid, start, end)
    dist = dict(zip(nocheat_path, range(nocheat_length)))

    bs = 5
    brange = list(range(-20 // bs, 20 // bs + 1))
    buckets = defaultdict(set)
    seen = set()
    for r, c in nocheat_path:
        buckets[r//bs, c//bs].add((r, c))
    
    nshort = 0
    for cheat_start in tqdm(nocheat_path, desc="Trying all cheats", leave=False):
        r, c = cheat_start
        br, bc = r//bs, c//bs
        for dr, dc in it.product(brange, repeat=2):
            for cheat_end in buckets[br+dr, bc+dc]:
                if cheat_start == cheat_end or (cheat_start, cheat_end) in seen:
                    continue
                cheat_length = manhattan(cheat_start, cheat_end)
                if cheat_length > 20:
                    continue
                if dist[cheat_start] > dist[cheat_end]:
                    cheat_start, cheat_end = cheat_end, cheat_start
                d = cheat_length + dist[cheat_start] + (dist[end] - dist[cheat_end])
                seen.add((cheat_end, cheat_start))
                if d <= nocheat_length - threshold:
                    nshort += 1
    return nshort

if __name__ == "__main__":
    print("Part 1 example", day20_part1("input/day20_example.txt", 0))
    print("Part 1", day20_part1("input/day20.txt", 100))
    print("Part 2 example", day20_part2("input/day20_example.txt", 50))
    print("Part 2", day20_part2("input/day20.txt", 100))
