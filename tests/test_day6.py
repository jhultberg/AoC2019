from aoc.day6 import calc_tree, num_orbits, find_parents, dist_between_orbits, solve

input = [
    ("COM", "B"),
    ("B", "C"),
    ("C", "D"),
    ("D", "E"),
    ("E", "F"),
    ("B", "G"),
    ("G", "H"),
    ("D", "I"),
    ("E", "J"),
    ("J", "K"),
    ("K", "L"),
]

input_with_santa = [
    ("COM", "B"),
    ("B", "C"),
    ("C", "D"),
    ("D", "E"),
    ("E", "F"),
    ("B", "G"),
    ("G", "H"),
    ("D", "I"),
    ("E", "J"),
    ("J", "K"),
    ("K", "L"),
    ("K", "YOU"),
    ("I", "SAN"),
]

tree = {
    "B": "COM",
    "C": "B",
    "D": "C",
    "E": "D",
    "F": "E",
    "G": "B",
    "H": "G",
    "I": "D",
    "K": "J",
    "L": "K",
    "J": "E",
}


def test_num_orbits():
    assert num_orbits(input) == 42


def test_calc_tree():
    assert calc_tree(input) == tree


def test_find_parents():
    assert find_parents(tree, "H") == {"G", "B", "COM"}


def test_dist_between_orbits():
    assert dist_between_orbits(input_with_santa, "SAN", "YOU") == 4


def test_solve():
    assert solve("data/day6.txt") == (241064, 418)
