from collections import Counter

def day01_part1(filename):
    with open(filename, "r") as f:
        ll = f.readlines()
    l1, l2 = list(), list()
    for l in ll:
        a, b = map(int, l.split())
        l1.append(a)
        l2.append(b)
    diff = 0
    for x, y in zip(sorted(l1), sorted(l2)):
        diff += abs(x - y)
    return diff

def day01_part2(filename):
    with open(filename, "r") as f:
        ll = f.readlines()
    l1 = list()
    ctr = Counter()
    for l in ll:
        a, b = map(int, l.split())
        l1.append(a)
        ctr[b] += 1
    similarity = 0
    for x in l1:
        similarity += x * ctr[x]
    return similarity
    
if __name__ == "__main__":
    print("Part 1 example", day01_part1("input/day01_example.txt"))
    print("Part 1", day01_part1("input/day01.txt"))
    print("Part 2 example", day01_part2("input/day01_example.txt"))
    print("Part 2", day01_part2("input/day01.txt"))
