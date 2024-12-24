from common import *
import operator as op

def parse_wires(lines):
    inputs = dict()
    wires = dict()

    for l in lines:
        if ":" in l:
            input, state = l.split(":")
            inputs[input] = int(state)
        else:
            l, output = l.split("->")
            inA, gate, inB = l.split()
            if inA > inB:
                inA, inB = inB, inA
            output = output.strip()
            wires[output] = (gate, inA, inB, set())
    
    for w in wires:
        _, inA, inB, _ = wires[w]
        if inA in wires:
            wires[inA][-1].add(w)
        if inB in wires:
            wires[inB][-1].add(w)
    return inputs, wires

def run_gates(wires, inputs, outputs):
    state = dict()
    for inp in inputs:
        state[inp] = inputs[inp]
        stack = list()
    for outp in outputs:
        stack.append(outp)

    while len(stack):
        wire = stack.pop()
        gate_type, inA, inB, _ = wires[wire]

        if inA in state and inB in state:
            state[wire] = operations[gate_type](state[inA], state[inB])
        else:
            stack.append(wire)
            stack.append(inA)
            stack.append(inB)
    return state

operations = {"AND": op.and_, "OR": op.or_, "XOR": op.xor}

def day24_part1(filename):
    lines = parse_lines(filename)
    inputs, wires = parse_wires(lines)
    outputs = [w for w in wires if w.startswith("z")]

    state = run_gates(wires, inputs, outputs)

    result = 0
    for outp in outputs:
        place = int(outp.strip("z"))
        result += state[outp] << place
    return result

def day24_part2(filename):
    lines = parse_lines(filename)
    inputs, wires = parse_wires(lines)
    outputs = [w for w in wires if w.startswith("z")]

    nbits = len(inputs) // 2
    suspects = set()
    for w in wires:
        gate, inA, inB, conn = wires[w]
        next_types = [wires[n][0] for n in conn]
        is_input = ("x" in inA and "y" in inB)
        is_first = inA == "x00" and inB == "y00"
        is_last = w == f"z{nbits:02d}"

        if "z" in w and gate != "XOR":
            if not is_last:
                suspects.add(w)
        if "z" not in w and gate == "XOR":
            if not is_input:
                suspects.add(w)
        if is_input and not is_first and gate == "XOR":
            if sorted(next_types) !=  ["AND", "XOR"]:
                suspects.add(w)
        if not is_first and gate == "AND":
            if "OR" not in next_types:
                suspects.add(w)
        
    return ",".join(sorted(suspects))

if __name__ == "__main__":
    print("Part 1 example", day24_part1("input/day24_example.txt"))
    print("Part 1 example 2", day24_part1("input/day24_example2.txt"))
    print("Part 1", day24_part1("input/day24.txt"))
    print("Part 2", day24_part2("input/day24.txt"))
