from aoc.day14 import calc_tree, num_ore, solve

reactions = [
    ("A", (10, [(10, "ORE")])),
    ("B", (1, [(1, "ORE")])),
    ("C", (1, [(7, "A"), (1, "B")])),
    ("D", (1, [(7, "A"), (1, "C")])),
    ("E", (1, [(7, "A"), (1, "D")])),
    ("FUEL", (1, [(7, "A"), (1, "E")])),
]

reactions_2 = [
    ("NZVS", (5, [(157, "ORE")])),
    ("DCFZ", (6, [(165, "ORE")])),
    (
        "FUEL",
        (
            1,
            [
                (44, "XJWVT"),
                (5, "KHKGT"),
                (1, "QDVJ"),
                (29, "NZVS"),
                (9, "GPVTF"),
                (48, "HKGWZ"),
            ],
        ),
    ),
    ("QDVJ", (9, [(12, "HKGWZ"), (1, "GPVTF"), (8, "PSHF")])),
    ("PSHF", (7, [(179, "ORE")])),
    ("HKGWZ", (5, [(177, "ORE")])),
    ("XJWVT", (2, [(7, "DCFZ"), (7, "PSHF")])),
    ("GPVTF", (2, [(165, "ORE")])),
    ("KHKGT", (8, [(3, "DCFZ"), (7, "NZVS"), (5, "HKGWZ"), (10, "PSHF")])),
]

reactions_3 = [
    ("STKFG", (1, [(2, "VPVL"), (7, "FWMGM"), (2, "CXFTF"), (11, "MNCFX")])),
    ("VPVL", (8, [(17, "NVRVD"), (3, "JNWZP")])),
    (
        "FUEL",
        (
            1,
            [
                (53, "STKFG"),
                (6, "MNCFX"),
                (46, "VJHF"),
                (81, "HVMC"),
                (68, "CXFTF"),
                (25, "GNMV"),
            ],
        ),
    ),
    ("FWMGM", (5, [(22, "VJHF"), (37, "MNCFX")])),
    ("NVRVD", (4, [(139, "ORE")])),
    ("JNWZP", (7, [(144, "ORE")])),
    (
        "HVMC",
        (3, [(5, "MNCFX"), (7, "RFSQX"), (2, "FWMGM"), (2, "VPVL"), (19, "CXFTF")]),
    ),
    ("GNMV", (6, [(5, "VJHF"), (7, "MNCFX"), (9, "VPVL"), (37, "CXFTF")])),
    ("MNCFX", (6, [(145, "ORE")])),
    ("CXFTF", (8, [(1, "NVRVD")])),
    ("RFSQX", (4, [(1, "VJHF"), (6, "MNCFX")])),
    ("VJHF", (6, [(176, "ORE")])),
]


tree = {
    "B": (1, [(1, "ORE")]),
    "C": (1, [(7, "A"), (1, "B")]),
    "D": (1, [(7, "A"), (1, "C")]),
    "E": (1, [(7, "A"), (1, "D")]),
    "FUEL": (1, [(7, "A"), (1, "E")]),
    "A": (10, [(10, "ORE")]),
}

tree_2 = {
    "A": (2, [(9, "ORE")]),
    "B": (3, [(8, "ORE")]),
    "C": (5, [(7, "ORE")]),
    "AB": (1, [(3, "A"), (4, "B")]),
    "BC": (1, [(5, "B"), (7, "C")]),
    "CA": (1, [(4, "C"), (1, "A")]),
    "FUEL": (1, [(2, "AB"), (3, "BC"), (4, "CA")]),
}


def test_calc_tree():
    assert calc_tree(reactions) == tree


def test_num_ore():
    # assert num_ore(tree) == 31
    # assert num_ore(tree_2) == 165
    assert num_ore(calc_tree(reactions_2)) == 13312
    assert num_ore(calc_tree(reactions_3)) == 180697


def _test_solve():
    assert solve("data/day14.txt") == (None, None)
