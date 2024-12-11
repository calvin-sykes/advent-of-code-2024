from common import *

def parse_trails(lines):
    topo_map = []
    trailheads = []
    for row, l in enumerate(lines):
        topo_map.append(list())
        for col, c in enumerate(l):
            if c == ".":
                topo_map[-1].append(100)
            else:
                topo_map[-1].append(int(c))
                if int(c) == 0:
                    trailheads.append((row, col))
    return topo_map, trailheads

def explore(topo_map, hikes, pos):
    h, w = len(topo_map), len(topo_map[0]) 
    r, c = pos
    h0 = topo_map[r][c]

    for d in range(4):
        nx, ny = r + D.dy[d], c + D.dx[d]
        if bounds((nx, ny), [(0, h), (0, w)]) and topo_map[nx][ny] == h0 + 1:
            new_hike = [((nx, ny), h0 + 1)]
            hikes.append(explore(topo_map, new_hike, (nx, ny)))
    return hikes

def judge_hike(hike, height9_pos=None):
    score = 0
    for elem in hike:
        if isinstance(elem, list):
            score += judge_hike(elem, height9_pos)
        elif elem[1] == 9:
            if height9_pos is None:
                score += 1
            elif elem[0] not in height9_pos:
                height9_pos.add(elem[0])
                score += 1
    return score

def day10_part1(filename):
    lines = parse_lines(filename)
    topo_map, trailheads = parse_trails(lines)

    total_score = 0
    for head in trailheads:
        hikes = explore(topo_map, [(head, 0)], head)
        total_score += judge_hike(hikes, set())
    return total_score

def day10_part2(filename):
    lines = parse_lines(filename)
    topo_map, trailheads = parse_trails(lines)

    total_rating = 0
    for head in trailheads:
        hikes = explore(topo_map, [(head, 0)], head)
        total_rating += judge_hike(hikes)
    return total_rating

if __name__ == "__main__":
    print("Part 1 example", day10_part1("input/day10_example.txt"))
    print("Part 1", day10_part1("input/day10.txt"))
    print("Part 2 example", day10_part2("input/day10_example.txt"))
    print("Part 2", day10_part2("input/day10.txt"))
