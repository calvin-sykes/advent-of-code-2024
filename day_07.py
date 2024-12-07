from common import *

from operator import add, mul
from math import log10, floor

def concat(a, b):
    scale = floor(log10(b)) + 1
    return 10**scale * a + b

def evaluate(op_list: list, operands: list):
    val = operands[0]
    for op, rhs in zip(op_list, operands[1:]):
        val = op(val, rhs)
    return val

def test_possible_operations(values, op_list):
    possible = 0
    for v in tqdm(values, leave=False):
        operands = values[v]
        nop = len(operands) - 1
        for ops in it.product(op_list, repeat=nop):
            res = evaluate(ops, operands)
            if res == v:
                possible += v
                break
    return possible

def day07_part1(filename):
    lines = parse_lines(filename)

    values = dict()
    for l in lines:
        value, operands = l.split(":")
        values[int(value)] = list(map(int, operands.split()))
    
    return test_possible_operations(values, [add, mul])

def day07_part2(filename):
    lines = parse_lines(filename)

    values = dict()
    for l in lines:
        value, operands = l.split(":")
        values[int(value)] = list(map(int, operands.split()))
    
    return test_possible_operations(values, [add, mul, concat])

if __name__ == "__main__":
    print("Part 1 example", day07_part1("input/day07_example.txt"))
    print("Part 1", day07_part1("input/day07.txt"))
    print("Part 2 example", day07_part2("input/day07_example.txt"))
    print("Part 2", day07_part2("input/day07.txt"))
