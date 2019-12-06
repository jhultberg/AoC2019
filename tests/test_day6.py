from aoc.day6 import (
    calc_tree,
    calc_center,
    calc_orbits,
    recursive_calc_orbits,
    calc_tree_child_to_parent,
    find_parents,
    dist_to_santa,
)

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
    "B": ["C", "G"],
    "C": ["D"],
    "COM": ["B"],
    "D": ["E", "I"],
    "E": ["F", "J"],
    "J": ["K"],
    "K": ["L"],
    "G": ["H"],
}

tree_from_child = {
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

test_data = [
    "COM)B",
    "B)C",
    "C)D",
    "D)E",
    "E)F",
    "B)G",
    "G)H",
    "D)I",
    "E)J",
    "J)K",
    "K)L",
    "K)YOU",
    "I)SAN",
]


def test_calc_tree():
    assert calc_tree(input) == tree


def test_calc_center():
    assert calc_center(
        {"COM", "B", "C", "D", "E", "G", "J", "K"},
        {"B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"},
    ) == {"COM"}


def test_recursive_calc_orbits():
    assert recursive_calc_orbits({"COM": ["A"]}, "COM", 0) == 1
    assert recursive_calc_orbits(tree, "COM", 0) == 42


def test_calc_orbits():
    assert calc_orbits(input, "COM") == 42


def test_calc_tree_child_to_parent():
    assert calc_tree_child_to_parent(input) == tree_from_child


def test_find_parents():
    assert find_parents(tree_from_child, "H", set()) == {"G", "B", "COM"}


def test_dist_to_santa():
    assert dist_to_santa(input_with_santa, "COM") == 4
