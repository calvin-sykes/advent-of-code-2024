from common import *

import re

def day03_part1(filename):
    lines = parse_lines(filename)
    lines = "".join(lines)

    regexp = re.compile("mul\((\d+),(\d+)\)")
    matches = re.findall(regexp, lines)
    sum = 0
    for m in matches:
        sum += int(m[0]) * int(m[1])
    return sum


def day03_part2(filename):
    lines = parse_lines(filename)
    lines = "".join(lines)
    
    regexp = re.compile("(do\(\)|don't\(\))|mul\((\d+),(\d+)\)")
    matches = re.findall(regexp, lines)
    sum = 0
    enabled = True
    for m in matches:
        if m[0]:
            enabled = "n't" not in m[0]
        elif enabled:
            sum += int(m[1]) * int(m[2])
    return sum

if __name__ == "__main__":
    print("Part 1 example", day03_part1("input/day03_example.txt"))
    print("Part 1", day03_part1("input/day03.txt"))
    print("Part 2 example", day03_part2("input/day03_part2_example.txt"))
    print("Part 2", day03_part2("input/day03.txt"))
