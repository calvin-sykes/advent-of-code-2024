from common import *

def day08_part1(filename):
    lines = parse_lines(filename)
    h, w = len(lines), len(lines[0])

    antennae = coll.defaultdict(set)
    for row, l in enumerate(lines):
        for col, c in enumerate(l):
            if c != ".":
                antennae[c].add((row, col))
    
    antinodes = set()
    for a in antennae:
        for (y1, x1), (y2, x2) in it.combinations(antennae[a], 2):
            dy = y2 - y1
            dx = x2 - x1
            if bounds((y1 - dy, x1 - dx), [(0, h), (0, w)]):
                antinodes.add((y1 - dy, x1 - dx))
            if bounds((y2 + dy, x2 + dx), [(0, h), (0, w)]):
                antinodes.add((y2 + dy, x2 + dx))

    return len(antinodes)

def day08_part2(filename):
    lines = parse_lines(filename)
    h, w = len(lines), len(lines[0])

    antennae = coll.defaultdict(set)
    for row, l in enumerate(lines):
        for col, c in enumerate(l):
            if c != ".":
                antennae[c].add((row, col))
    
    antinodes = set()
    for a in antennae:
        for (y1, x1), (y2, x2) in it.combinations(antennae[a], 2):
            dy = y2 - y1
            dx = x2 - x1

            step = 0
            while True:
                newy = y1 - dy * step
                newx = x1 - dx * step
                if bounds((newy, newx), [(0, h), (0, w)]):
                    antinodes.add((newy, newx))
                    step += 1   
                else:
                    break

            step = 0
            while True:
                newy = y2 + dy * step
                newx = x2 + dx * step
                if bounds((newy, newx), [(0, h), (0, w)]):
                    antinodes.add((newy, newx))
                    step += 1
                else:
                    break

    return len(antinodes)

if __name__ == "__main__":
    print("Part 1 example", day08_part1("input/day08_example.txt"))
    print("Part 1", day08_part1("input/day08.txt"))
    print("Part 2 example", day08_part2("input/day08_example.txt"))
    print("Part 2", day08_part2("input/day08.txt"))
