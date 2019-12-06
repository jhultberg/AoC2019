def calc_tree(input):
    tree = {}
    for objects in input:
        if objects[0] in tree:
            tree[objects[0]].append(objects[1])
        else:
            tree[objects[0]] = [objects[1]]
    return tree


def calc_tree_child_to_parent(input):
    tree = {}
    for objects in input:
        tree[objects[1]] = objects[0]
    return tree


def calc_center(left, right):
    return left - right


def recursive_calc_orbits(tree, node, depth):
    if node not in tree:
        return depth
    else:
        orbits = 0
        for child in tree[node]:
            orbits += recursive_calc_orbits(tree, child, depth + 1)
    return orbits + depth


def calc_orbits(input, center):
    tree = calc_tree(input)
    return recursive_calc_orbits(tree, center, 0)


def find_parents(tree, node, parents):
    if node not in tree:
        return parents
    else:
        parents.add(tree[node])
        return find_parents(tree, tree[node], parents)


def dist_to_santa(input, center):
    tree = calc_tree_child_to_parent(input)
    santa = find_parents(tree, "SAN", set())
    you = find_parents(tree, "YOU", set())
    distance = len(santa ^ you)
    return distance


def solve(path):
    input = []
    with open(path) as f:
        left = set()
        right = set()
        for line in f:
            points = line.strip().split(")")
            input.append((points[0], points[1]))
            left.add(points[0])
            right.add(points[1])
        center = calc_center(left, right)

    center = center.pop()
    a = calc_orbits(input, center)
    b = dist_to_santa(input, center)
    return (a, b)
