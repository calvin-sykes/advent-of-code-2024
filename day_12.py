from common import *

def find_regions(lines):
    h, w = len(lines), len(lines[0])
    regions = defaultdict(set)
    seen = set()
    
    for base_row, l in enumerate(lines):
        for base_col, c in enumerate(l):
            if (base_row, base_col) in seen:
                continue
            else:
                key = (base_row, base_col, c)
                stack = [(base_row, base_col)]
                while len(stack):
                    row, col = stack.pop()
                    regions[key].add((row, col))
                    seen.add((row, col))
                    for d in range(4):
                        nr, nc = row + D.dy[d], col + D.dx[d]
                        if bounds([nr, nc], [(0, h), (0, w)]) and lines[nr][nc] == c and (nr, nc) not in seen:
                            stack.append((nr, nc))
    return regions

def day12_part1(filename):
    lines = parse_lines(filename)
    h, w = len(lines), len(lines[0])
    regions = find_regions(lines)

    fences = 0
    for base in regions:
        *_, l = base
        perimeter = 0
        area = len(regions[base])
        for (pr, pc) in regions[base]:
            for d in range(4):
                nr, nc = pr + D.dy[d], pc + D.dx[d]
                if bounds([nr, nc], [(0, h), (0, w)]):
                    if lines[nr][nc] != l:
                        perimeter += 1
                else:
                    perimeter += 1
        fences += area * perimeter
    return fences

def day12_part2(filename):
    lines = parse_lines(filename)
    h, w = len(lines), len(lines[0])
    regions = find_regions(lines)

    fences = 0
    for base in regions:
        *_, l = base
        area = len(regions[base])
        sides = 0

        for (pr, pc) in sorted(regions[base]):
            ngb = set()
            for d in range(4):
                nr, nc = pr + D.dy[d], pc + D.dx[d]
                if bounds([nr, nc], [(0, h), (0, w)]):
                    if lines[nr][nc] == l:
                        ngb.add((D.dy[d], D.dx[d]))
            n_ngb = len(ngb)
            if n_ngb == 4: # + shape
                corners = 4
                for (cr, cc) in {(1, 1), (1, -1), (-1, 1), (-1, -1)}:
                    nr, nc = pr + cr, pc + cc
                    if bounds([nr, nc], [(0, h), (0, w)]):
                        if (nr, nc) in regions[base]:
                            corners -= 1
            elif n_ngb == 3: # T shape
                corners = 2
                c1, c2, c3 = ngb
                for (c1, c2) in it.combinations(ngb, 2):
                    cr, cc = c1[0] + c2[0], c1[1] + c2[1]
                    if cr == 0 and cc == 0:
                        continue
                    nr, nc = pr + cr, pc + cc
                    if (nr, nc) in regions[base]:
                        corners -= 1
            elif n_ngb == 2: # either straight edge, or L shape
                if (ngb == {(0, 1), (0, -1)}) or (ngb == {(1, 0), (-1, 0)}):
                    corners = 0
                else:
                    c1, c2 = ngb
                    cr, cc = c1[0] + c2[0], c1[1] + c2[1]
                    nr, nc = pr + cr, pc + cc
                    if (nr, nc) in regions[base]:
                        corners = 1
                    else:
                        corners = 2
            elif n_ngb == 1: # peninsula
                corners = 2
            else: # isolated
                corners = 4
            sides += corners
        fences += area * sides
    return fences

if __name__ == "__main__":
    print("Part 1 example 1", day12_part1("input/day12_example1.txt"))
    print("Part 1 example 2", day12_part1("input/day12_example2.txt"))
    print("Part 1 example 3", day12_part1("input/day12_example3.txt"))
    print("Part 1", day12_part1("input/day12.txt"))
    print("Part 2 example 1", day12_part2("input/day12_example1.txt"))
    print("Part 2 example 2", day12_part2("input/day12_example2.txt"))
    print("Part 2 example 2b", day12_part2("input/day12_example2b.txt"))
    print("Part 2 example 3", day12_part2("input/day12_example3.txt"))
    print("Part 2", day12_part2("input/day12.txt"))
