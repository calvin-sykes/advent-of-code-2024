from collections import Counter

from common import *

def day01_part1(filename):
    lines = parse_lines(filename)
    l1, l2 = list(), list()
    for l in lines:
        a, b = map(int, l.split())
        l1.append(a)
        l2.append(b)
    diff = sum(abs(x - y) for x, y in zip(sorted(l1), sorted(l2)))
    return diff

def day01_part2(filename):
    lines = parse_lines(filename)
    l1, l2 = list(), list()
    for l in lines:
        a, b = map(int, l.split())
        l1.append(a)
        l2.append(b)
    ctr = Counter(l2)
    similarity = sum(x * ctr[x] for x in l1)
    return similarity
    
if __name__ == "__main__":
    print("Part 1 example", day01_part1("input/day01_example.txt"))
    print("Part 1", day01_part1("input/day01.txt"))
    print("Part 2 example", day01_part2("input/day01_example.txt"))
    print("Part 2", day01_part2("input/day01.txt"))
