def calc_tree(input):
    return {c: p for p, c in input}


def num_orbits(input):
    tree = calc_tree(input)
    return sum(len(set(find_parents(tree, node))) for node in tree)


def find_parents(tree, node):
    while node in tree:
        node = tree[node]
        yield node


def dist_between_orbits(input, first_planet, second_planet):
    tree = calc_tree(input)
    first_route = set(find_parents(tree, first_planet))
    second_route = set(find_parents(tree, second_planet))
    return len(first_route ^ second_route)


def solve(path):
    with open(path) as f:
        input = list(line.strip().split(")") for line in f)

    a = num_orbits(input)
    b = dist_between_orbits(input, "SAN", "YOU")
    return (a, b)
