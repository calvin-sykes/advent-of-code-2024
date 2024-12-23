from common import *

def find_cliques(network, size):
    groups = set()
    for node in network:
        for others in it.combinations(network[node], size-1):
            for o1, o2 in it.combinations(others, 2):
                if o1 not in network[o2]:
                    break
            else:
                groups.add(frozenset(others + (node,)))
    return groups

def find_maximum_clique(network):
    def bron_kerbosch(r : set, p : set, x : set):
        cliques = []
        if len(p) == len(x) == 0:
            cliques.append(r)
        else:
            pivot = max(p.union(x), key=lambda u: len(network[u]))
            for v in p.difference(network[pivot]):
                cliques.extend(bron_kerbosch(r.union({v}),
                    p.intersection(network[v]), x.intersection(network[v])))
                p.remove(v)
                x.add(v)
        return cliques    
    return max(bron_kerbosch(set(), set(network), set()), key=len)

def day23_part1(filename):
    lines = parse_lines(filename)

    network = defaultdict(set)
    for l in lines:
        to, frm = l.split("-")
        network[to].add(frm)
        network[frm].add(to)

    num_nets = 0
    cliques = find_cliques(network, 3)
    for clique in cliques:
        if any(s.startswith("t") for s in clique):
            num_nets += 1
    return num_nets

def day23_part2(filename):
    lines = parse_lines(filename)

    network = defaultdict(set)
    for l in lines:
        to, frm = l.split("-")
        network[to].add(frm)
        network[frm].add(to)

    clique = find_maximum_clique(network)
    return ",".join(sorted(clique))

if __name__ == "__main__":
    print("Part 1 example", day23_part1("input/day23_example.txt"))
    print("Part 1", day23_part1("input/day23.txt"))
    print("Part 2 example", day23_part2("input/day23_example.txt"))
    print("Part 2", day23_part2("input/day23.txt"))
