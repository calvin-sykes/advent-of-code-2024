from common import *

def isclose(x):
    reltol = abs(x - round(x)) / x < 1e-6
    abstol = abs(x - round(x)) < 1e-3
    return reltol and abstol

def parse_machines(lines, part2):
    machines = []
    for l in lines:
        l1, l2 = l.split(":")
        if l1 == "Button A":
            m = {}
            x, y = map(lambda s: int(s[2:]), l2.split(","))
            m["A"] = (x, y)
        elif l1 == "Button B":
            x, y = map(lambda s: int(s[2:]), l2.split(","))
            m["B"] = (x, y)
        elif l1 == "Prize":
            x, y = map(lambda s: int(s[3:]), l2.split(","))
            if part2:
                x += 10000000000000
                y += 10000000000000
            m["P"] = (x, y)
            machines.append(m)
    return machines

def day13(filename, part2=False):
    lines = parse_lines(filename)
    machines = parse_machines(lines, part2)
    
    total_cost = 0
    for m in machines:
        # nA * (Ax, Ay) + nB * (Bx, By) = (Px, Py)
        matrix = [[m["A"][0], m["B"][0]], 
                  [m["A"][1], m["B"][1]]]
        prize = m["P"]
        determinant = (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
        idt = 1.0 / determinant
        inverse = [[idt * matrix[1][1], -idt * matrix[0][1]],
                   [-idt * matrix[1][0], idt * matrix[0][0]]]
        solution = [inverse[0][0] * prize[0] + inverse[0][1] * prize[1],
                    inverse[1][0] * prize[0] + inverse[1][1] * prize[1]]
        if all(map(isclose, solution)):
            total_cost += round(3 * solution[0] + solution[1])
    return total_cost

if __name__ == "__main__":
    print("Part 1 example", day13("input/day13_example.txt"))
    print("Part 1", day13("input/day13.txt"))
    print("Part 2 example", day13("input/day13_example.txt", True))
    print("Part 2", day13("input/day13.txt", True))
