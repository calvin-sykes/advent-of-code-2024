from common import *
    

def day09_part1(filename):
    line, = parse_lines(filename)

    id = 0
    disk = []
    for i, c in enumerate(line):
        if i % 2 == 0:
            disk.extend([id] * int(c))
            id += 1
        else:
            disk.extend("." * int(c))

    first_space = 0
    while disk[first_space] != ".":
        first_space += 1
    last_file = len(disk) - 1
    while disk[last_file] == ".":
        last_file -= 1

    while first_space < last_file:
        disk[first_space] = disk[last_file]
        disk[last_file] = "."
        while disk[first_space] != ".":
            first_space += 1
        while disk[last_file] == ".":
            last_file -= 1

    checksum = sum(i * c for i, c in enumerate(disk) if c != ".")
    return checksum 
    
def day09_part2(filename):
    line, = parse_lines(filename)

    id = 0
    pos = 0
    files = []
    spaces = []
    for i, c in enumerate(line):
        cc = int(c)
        if i % 2 == 0:
            files.append((id, pos, cc))
            id += 1
        else:
            spaces.append((pos, cc))
        pos += cc

    for (id, file_start, file_length) in files[::-1]:
        for ispc, (space_start, space_length) in enumerate(spaces):
            if file_start < space_start:
                break
            if space_length >= file_length:
                files[id] = (id, space_start, file_length)
                spaces[ispc] = (space_start + file_length, space_length - file_length)
                break

    checksum = 0
    for (id, file_start, file_length) in files:
        for i in range(file_length):
            checksum += id * (file_start + i)
    return checksum

if __name__ == "__main__":
    print("Part 1 example", day09_part1("input/day09_example.txt"))
    print("Part 1", day09_part1("input/day09.txt"))
    print("Part 2 example", day09_part2("input/day09_example.txt"))
    print("Part 2", day09_part2("input/day09.txt"))
