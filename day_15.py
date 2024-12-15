from common import *

def parse_grid(lines, part2=False):
    widen = {"#": "##", "O": "[]", ".": "..", "@": "@."}
    grid = []
    turtle = []
    for r, l in enumerate(lines):
        if "#" in l:
            if "@" in l:
                c = l.index("@")
                if part2: c *= 2
                robot = (r, c)
            if part2:
                grid.append(list("".join(widen[c] for c in l)))
            else:
                grid.append(list(l))
        else:
            turtle.append(l)
    turtle = "".join(turtle)
    return grid, turtle, robot

def can_move(grid, pos, dir, moves_list):
    r, c = pos
    dr, dc = D.dy[dir], D.dx[dir]
    nr, nc = r + dr, c + dc

    if (nr, nc) in moves_list:
        success = True
        if (r, c) not in moves_list:
            moves_list.append((r, c))
    elif grid[nr][nc] == ".":
        success = True
        moves_list.append((r, c))
    elif grid[nr][nc] == "#":
        success = False
    elif grid[nr][nc] == "[":
        success = can_move(grid, (nr, nc+1), dir, moves_list) and \
            can_move(grid, (nr, nc), dir, moves_list)
        if success:
            moves_list.append((r, c))
            if (r,c+1) not in moves_list and grid[r][c+1] == "]":
                moves_list.append((r, c+1))
    elif grid[nr][nc] == "]":
        success = can_move(grid, (nr, nc-1), dir, moves_list) and \
            can_move(grid, (nr, nc), dir, moves_list)
        if success:
            moves_list.append((r, c))
            if (r,c-1) not in moves_list and grid[r][c-1] == "[":
                moves_list.append((r, c-1))
    else:
        success = can_move(grid, (nr, nc), dir, moves_list)
        if success:
            moves_list.append((r, c))
    return success

def try_move(grid, pos, dir):
    r, c = pos
    dr, dc = D.dy[dir], D.dx[dir]

    to_move = []
    success = can_move(grid, pos, dir, to_move)

    if success:
        for (r, c) in to_move:
            nr, nc = r + dr, c + dc
            grid[nr][nc] = grid[r][c]
            grid[r][c] = "."
    return success

def sum_gps(grid, boxchar="O"):
    gps = 0
    for row, l in enumerate(grid):
        for col, c in enumerate(l):
            if c == boxchar:
                gps += 100 * row + col
    return gps

def day15_part1(filename):
    lines = parse_lines(filename)
    grid, turtle, robot = parse_grid(lines)

    for move in turtle:
        dir = D.directions.index(move)
        if try_move(grid, robot, dir):
            r, c = robot
            robot = r + D.dy[dir], c + D.dx[dir]
    return sum_gps(grid)

def day15_part2(filename):
    lines = parse_lines(filename)
    grid, turtle, robot = parse_grid(lines, True)

    for move in turtle:
        dir = D.directions.index(move)
        if try_move(grid, robot, dir):
            r, c = robot
            robot = r + D.dy[dir], c + D.dx[dir]
    return sum_gps(grid, "[")

if __name__ == "__main__":
    print("Part 1 example", day15_part1("input/day15_example.txt"))
    print("Part 1 example 2", day15_part1("input/day15_example2.txt"))
    print("Part 1", day15_part1("input/day15.txt"))
    print("Part 2 example", day15_part2("input/day15_example3.txt"))
    print("Part 2 example 2", day15_part2("input/day15_example2.txt"))
    print("Part 2", day15_part2("input/day15.txt"))
