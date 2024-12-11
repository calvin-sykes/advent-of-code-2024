from common import *
from math import floor, log10
from functools import cache

def blink_one(stone):
    if stone == 0:
        return (1, None)
    elif (p := (floor(log10(stone))) + 1) % 2 == 0:
        halfpow = 10**(p//2)
        lower_digits = stone % halfpow
        upper_digits = (stone - lower_digits) // halfpow
        return (upper_digits, lower_digits)
    else:
        return (stone * 2024, None)

def blink(stones):
    newstones = []
    for s in stones:
        l, r = blink_one(s)
        newstones.append(l)
        if r is not None:
            newstones.append(r)
    return newstones

@cache
def blink_recursive(stone, blinks_remaining):
    left, right = blink_one(stone)

    if blinks_remaining == 1:
        return 1 + (right is not None)
    else:
        n = blink_recursive(left, blinks_remaining - 1)
        if right is not None:
            n += blink_recursive(right, blinks_remaining - 1)
    return n

def day11_part1(filename, n_blinks):
    line, = parse_lines(filename)
    stones = list(map(int, line.split()))

    for _ in range(n_blinks):
        stones = blink(stones)
    return len(stones)

def day11_part2(filename, n_blinks):
    line, = parse_lines(filename)
    stones = list(map(int, line.split()))

    return sum(blink_recursive(s, n_blinks) for s in stones)

if __name__ == "__main__":
    print("Part 1 example", day11_part1("input/day11_example.txt", 25))
    print("Part 1", day11_part1("input/day11.txt", 25))
    print("Part 2 example", day11_part2("input/day11_example.txt", 75))
    print("Part 2", day11_part2("input/day11.txt", 75))
