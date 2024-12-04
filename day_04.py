from common import *

def check_word(lines, coords, lookword="XMAS"):
    try:
        word = "".join(lines[r][c] for r, c in coords)
    except IndexError:
        return False
    return word == lookword

def check_xmas(lines, a_coord):
    i, j = a_coord
    h, w = len(lines), len(lines[0])
    assert lines[i][j] == "A"

    pdiag = []
    ndiag = []
    for k in [-1, 0, 1]:
        ii = i + k
        jjp = j + k
        jjn = j - k
        if not bounds([ii, jjp, jjn], [(0, h), (0, w), (0, w)]):
            return False
        pdiag.append((ii, jjp))
        ndiag.append((ii, jjn))

    return (check_word(lines, pdiag, "MAS") or check_word(lines, pdiag, "SAM")) and \
            (check_word(lines, ndiag, "MAS") or check_word(lines, ndiag, "SAM"))

def day04_part1(filename):
    lines = parse_lines(filename)
    h, w = len(lines), len(lines[0])

    words = 0
    for i in range(h):
        for j in range(w):
            if lines[i][j] != "X":
                continue
            for xdir, ydir in it.product([-1, 0, 1], repeat=2):
                if xdir == 0 and ydir == 0:
                    continue
                coords = []
                for k in range(4):
                    ii = i + ydir * k
                    jj = j + xdir * k
                    if not bounds([ii, jj], [(0, h), (0, w)]):
                        break
                    coords.append((ii, jj))
                else:
                    if check_word(lines, coords):
                        words += 1
    return words

def day04_part2(filename):
    lines = parse_lines(filename)
    h, w = len(lines), len(lines[0])

    xmases = 0
    for i in range(h):
        for j in range(w):
            if lines[i][j] == "A" and check_xmas(lines, (i, j)):
                xmases += 1
    return xmases

if __name__ == "__main__":
    print("Part 1 example", day04_part1("input/day04_example.txt"))
    print("Part 1", day04_part1("input/day04.txt"))
    print("Part 2 example", day04_part2("input/day04_example.txt"))
    print("Part 2", day04_part2("input/day04.txt"))
