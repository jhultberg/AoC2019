from aoc.day18 import Maze, parse_input
from collections import deque

input = ["#########", "#b.A.@.a#", "#########"]

input2 = ["########################",
"#f.D.E.e.C.b.A.@.a.B.c.#",
"######################.#",
"#d.....................#",
"########################"]

walls = {
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (6, 0),
    (7, 0),
    (8, 0),
    (0, 1),
    (8, 1),
    (0, 1),
    (8, 1),
    (0, 2),
    (1, 2),
    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2),
    (6, 2),
    (7, 2),
    (8, 2),
}
keys = {(1, 1): "b", (7, 1): "a"}
doors = {(3, 1): "A"}
name_to_doors = {"A": (3, 1)}
position = (5, 1)

maze = Maze(walls, doors, name_to_doors, keys, position)

maze2 = parse_input(input2)


def test_parse_input():
    assert parse_input(input) == maze


def test_find_neighbors():
    assert maze.find_neighbors(set()) == deque([(6, 1), (4, 1)])


def test_collect_all_keys():
    assert maze2.collect_all_keys() == 8
