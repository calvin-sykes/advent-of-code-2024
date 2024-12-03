from common import *

def sgn(x):
    return 1 if x > 0 else -1

def issafe(report):
    s = 0
    for a, b in zip(report, report[1:]):
        d = b - a
        if s and sgn(d) != s:
            return False
        s = sgn(d)
        if abs(d) < 1 or abs(d) > 3:
            return False
    return True
    
def day02_part1(filename):
    lines = parse_lines(filename)
    reports = [list(map(int, l.split())) for l in lines]
    
    safe = sum(map(issafe, reports))
    return safe

def day02_part2(filename):
    lines = parse_lines(filename)
    reports = [list(map(int, l.split())) for l in lines]
    
    safe = 0
    for r in reports:
        if issafe(r):
            safe += 1
        else:
            for i in range(len(r)):
                rr = [l for j, l in enumerate(r) if j != i]
                if issafe(rr):
                    safe += 1
                    break
    return safe

if __name__ == "__main__":
    print("Part 1 example", day02_part1("input/day02_example.txt"))
    print("Part 1", day02_part1("input/day02.txt"))
    print("Part 2 example", day02_part2("input/day02_example.txt"))
    print("Part 2", day02_part2("input/day02.txt"))
