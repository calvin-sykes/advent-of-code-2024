def parse_lines(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return [l.rstrip("\n") for l in lines if l.strip()]
