from aoc.day22 import shuffle, parse_input, solve

input = ["deal with increment 7\n", "deal into new stack\n", "deal into new stack\n"]


input2 = ["cut 6\n", "deal with increment 7\n", "deal into new stack\n"]

input3 = ["deal with increment 7\n", "deal with increment 9\n", "cut -2\n"]

input4 = [
    "deal into new stack\n",
    "cut -2\n",
    "deal with increment 7\n",
    "cut 8\n",
    "cut -4\n",
    "deal with increment 7\n",
    "cut 3\n",
    "deal with increment 9\n",
    "deal with increment 3\n",
    "cut -1\n",
]


def test_parse_input():
    assert parse_input(input) == [("incr", 7), ("stack", None), ("stack", None)]
    assert parse_input(input2) == [("cut", 6), ("incr", 7), ("stack", None)]


def test_shuffle():
    assert shuffle(parse_input(input), list(range(10))) == [
        0,
        3,
        6,
        9,
        2,
        5,
        8,
        1,
        4,
        7,
    ]
    assert shuffle(parse_input(input2), list(range(10))) == [
        3,
        0,
        7,
        4,
        1,
        8,
        5,
        2,
        9,
        6,
    ]
    assert shuffle(parse_input(input3), list(range(10))) == [
        6,
        3,
        0,
        7,
        4,
        1,
        8,
        5,
        2,
        9,
    ]
    assert shuffle(parse_input(input4), list(range(10))) == [
        9,
        2,
        5,
        8,
        1,
        4,
        7,
        0,
        3,
        6,
    ]
