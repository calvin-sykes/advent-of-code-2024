from common import *

def fits(lock, key):
    return all(l + k <= 5 for l, k in zip(lock, key))

def day25_part1(filename):
    lines = parse_lines(filename)
    lines.append(list())
    locks = []
    keys = []
    ll = None
    for i, l in enumerate(lines):
        if i % 7 == 0:
            if ll:
                pins = []
                for i in range(5):
                    pin = sum(ll[j][i] == "#" for j in range(7))
                    pins.append(pin - 1)
                if ll[0] == "#####":
                    locks.append(tuple(pins))
                elif ll[0] == ".....":
                    keys.append(tuple(pins))
            ll = []
        ll.append(l)
    
    matches = 0
    for l in locks:
        for k in keys:
            if fits(l, k):
                matches += 1
    return matches

if __name__ == "__main__":
    print("Part 1 example", day25_part1("input/day25_example.txt"))
    print("Part 1", day25_part1("input/day25.txt"))
