from common import *
from functools import reduce
from operator import mul

def parse_robots(lines):
    robots = []
    for l in lines[1:]:
        parts = l.split("=")
        p = list(map(int, parts[1].split()[0].split(",")))
        v = list(map(int, parts[2].split(",")))
        robots.append([p, v])
    w, h = map(int, lines[0].split(","))
    return robots, w, h

def plot_robots(robots, w, h):
    grid = [["."] * w for _ in range(h)]
    for r in robots:
        px, py = r[0]
        if grid[py][px] == ".":
            grid[py][px] = 1
        else:
            grid[py][px] += 1
    print("\n".join(["".join(map(str, grid[r])) for r in range(h)]))

def find_biggest_cluster(positions, w, h):
    positions = set(positions)
    seen = set()
    
    maxsize = 0
    for p in positions:
        if p in seen:
            continue
        else:
            size = 0
            stack = [p]
            while len(stack):
                x, y = stack.pop()
                size += 1
                seen.add((x, y))
                for d in range(4):
                    nx, ny = x + D.dx[d], y + D.dy[d]
                    if (nx, ny) in positions and (nx, ny) not in seen:
                        stack.append((nx, ny))
            maxsize = max(size, maxsize)
    return maxsize

def day14_part1(filename):
    lines = parse_lines(filename)
    robots, w, h = parse_robots(lines)
    
    t = 100
    for _ in range(t):
        for r in robots:
            vx, vy = r[1]
            px = (r[0][0] + vx) % w
            py = (r[0][1] + vy) % h
            r[0] = [px, py]

    counts = [0] * 4
    mx, my = w // 2, h // 2
    for r in robots:
        px, py = r[0]
        if px == mx or py == my:
            continue
        q = (px > w // 2) + 2 * (py > h // 2)
        counts[q] += 1
    return reduce(mul, counts)
    
def day14_part2(filename):
    lines = parse_lines(filename)
    robots, w, h = parse_robots(lines)

    possible_positions = []
    for r in robots:
        px, py = r[0]
        vx, vy = r[1]
        pos = [(px, py)]
        for _ in range(w * h):
            px = (px + vx) % w
            py = (py + vy) % h
            pos.append((px, py))
        possible_positions.append(pos)

    max_i = 0
    max_size = 0
    for i, pos in enumerate(tqdm(zip(*possible_positions), desc="Hunting for Easter egg", total=w*h, leave=False)):
        cluster_size = find_biggest_cluster(pos, w, h)
        if cluster_size > max_size:
            max_i = i
            max_size = cluster_size 
    max_robots = [(pos[max_i],) for pos in possible_positions]

    plot_robots(max_robots, w, h)
    return max_i

if __name__ == "__main__":
    print("Part 1 example", day14_part1("input/day14_example.txt"))
    print("Part 1", day14_part1("input/day14.txt"))
    # print("Part 2 example", day14_part2("input/day14_example.txt"))
    print("Part 2", day14_part2("input/day14.txt"))
