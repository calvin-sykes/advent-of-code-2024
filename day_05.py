from common import *

def parse_pages(lines):
    rules = []
    updates = []
    for l in lines:
        if "|" in l:
            rules.append(tuple(map(int, l.split("|"))))
        else:
            updates.append(list(map(int, l.split(","))))

    before = defaultdict(set)
    for b, a in rules:
        before[a].add(b)
    return updates, before

def checkorder(upd, before):
    is_ordered = True
    updset = set(upd)
    for i, page in enumerate(upd):
        nbef = len(before[page] & updset)
        if nbef != i:
            is_ordered = False
            break
    return is_ordered

def reorder(upd, before):
    updset = set(upd)
    rightorder = [0] * len(upd)
    for page in upd:
        position = len(before[page] & updset)
        rightorder[position] = page
    return rightorder

def day05_part1(filename):
    lines = parse_lines(filename)
    updates, before = parse_pages(lines)

    midpages = 0
    for upd in updates:
        if checkorder(upd, before):
            midpages += upd[len(upd)//2]
    return midpages

def day05_part2(filename):
    lines = parse_lines(filename)
    updates, before = parse_pages(lines)

    midpages = 0
    for upd in updates:
        if not checkorder(upd, before):
            rightorder = reorder(upd, before)
            midpages += rightorder[len(upd)//2]
    return midpages    

if __name__ == "__main__":
    print("Part 1 example", day05_part1("input/day05_example.txt"))
    print("Part 1", day05_part1("input/day05.txt"))
    print("Part 2 example", day05_part2("input/day05_example.txt"))
    print("Part 2", day05_part2("input/day05.txt"))
