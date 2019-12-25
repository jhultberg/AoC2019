from aoc.day24 import (
    parse_input,
    biodiversity,
    next_state,
    biodiversity_rating,
    recursive_biodiversity,
    solve,
)

initial = ["....#", "#..#.", "#..##", "..#..", "#...."]

second_state = ["#..#.", "####.", "###.#", "##.##", ".##.."]

third_state = ["#####", "....#", "....#", "...#.", "#.###"]

repeated = [".....", ".....", ".....", "#....", ".#..."]


def test_parse_input():
    assert parse_input(initial) == (
        {
            (0, 0): 0,
            (1, 0): 0,
            (2, 0): 0,
            (3, 0): 0,
            (4, 0): 1,
            (0, 1): 1,
            (1, 1): 0,
            (2, 1): 0,
            (3, 1): 1,
            (4, 1): 0,
            (0, 2): 1,
            (1, 2): 0,
            (2, 2): 0,
            (3, 2): 1,
            (4, 2): 1,
            (0, 3): 0,
            (1, 3): 0,
            (2, 3): 1,
            (3, 3): 0,
            (4, 3): 0,
            (0, 4): 1,
            (1, 4): 0,
            (2, 4): 0,
            (3, 4): 0,
            (4, 4): 0,
        }
    )


def test_next_state():
    assert next_state(parse_input(initial)) == parse_input(second_state)
    assert next_state(parse_input(second_state)) == parse_input(third_state)


def test_biodiversity_rating():
    assert biodiversity_rating(parse_input(repeated)) == 2129920


def test_recursive_biodiversity():
    assert recursive_biodiversity(parse_input(initial), 10) == 99


def test_solve():
    assert solve("data/day24.txt") == (1151290, 1953)
