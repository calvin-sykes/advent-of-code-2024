from common import *
from functools import cache

def arrange_towels(design, patterns, part2=False):
    ld = len(design)

    @cache
    def count_arrangements(design, i):
        if i == ld:
            return 1
        ways = 0
        for p, l in patterns:
            if design[i:i+l] == p:
                ways += count_arrangements(design, i+l)
        return ways

    ways = count_arrangements(design, 0)
    return ways if part2 else (ways > 0)

def day19_part1(filename):
    lines = parse_lines(filename)
    patterns = [(pp := p.strip(), len(pp)) for p in lines[0].split(",")]
    designs = lines[1:]

    return sum(arrange_towels(d, patterns) for d in designs)

def day19_part2(filename):
    lines = parse_lines(filename)
    patterns = [(pp := p.strip(), len(pp)) for p in lines[0].split(",")]
    designs = lines[1:]

    return sum(arrange_towels(d, patterns, True) for d in designs)

if __name__ == "__main__":
    print("Part 1 example", day19_part1("input/day19_example.txt"))
    print("Part 1", day19_part1("input/day19.txt"))
    print("Part 2 example", day19_part2("input/day19_example.txt"))
    print("Part 2", day19_part2("input/day19.txt"))
