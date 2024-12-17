from common import *

def parse_program(lines):
    input = []
    for l in lines:
        l = l.split(":")[-1]
        if "," in l:
            input.append(list(map(int, l.split(","))))
        else:
            input.append(int(l))
    return input

def execute(A, B, C, prog):
    def combo(operand):
        if operand < 4:
            return operand
        else:
            return [A, B, C][operand-4]
    
    output = []
    ip = 0
    lp = len(prog)
    while ip < lp:
        opcode, operand = prog[ip], prog[ip+1]
        match opcode:
            case 0: # adv
                A = A // 2**combo(operand)
            case 1: # bxl
                B ^= operand
            case 2: # bst
                B = combo(operand) % 8
            case 3: # jnz
                if A != 0:
                    ip = operand
                    continue
            case 4: # bxc
                B ^= C
            case 5: # out
                output.append(combo(operand) % 8)
            case 6: # bdv
                B = A // 2**combo(operand)
            case 7: # cdv
                C = A // 2**combo(operand)
        ip += 2
    return output

def dfs_quine(A, B, C, program, digit, Adigits):
    if digit < 0:
        return True

    for i in range(8):
        output = execute(A + i, B, C, program)
        if output[0] == program[digit]:
            newA = A + i << 3
            Adigits.append(i)
            if dfs_quine(newA, B, C, program, digit-1, Adigits):
                return True
            Adigits.pop()
    return False

def day17_part1(filename):
    lines = parse_lines(filename)
    input = parse_program(lines)
    
    output = execute(*input)
    return ",".join(map(str, output))

def day17_part2(filename):
    lines = parse_lines(filename)
    _, B, C, program = parse_program(lines)

    Adigits = []
    if dfs_quine(0, B, C, program, len(program)-1, Adigits):
        A = int(str("".join(map(str, Adigits))), 8)
    else:
        raise ValueError("No quine possible (?)")
    return A

if __name__ == "__main__":
    print("Part 1 example", day17_part1("input/day17_example.txt"))
    print("Part 1", day17_part1("input/day17.txt"))
    print("Part 2 example", day17_part2("input/day17_example2.txt"))
    print("Part 2", day17_part2("input/day17.txt"))
