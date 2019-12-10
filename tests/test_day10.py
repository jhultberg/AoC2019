import pytest
from aoc.day10 import (
    is_colinear,
    find_angle_from_vertical,
    find_stars,
    find_asteroids,
    is_between_points,
    destroy_asteroids,
    solve,
    find_most_asteroids,
)


input = [".#..#", ".....", "#####", "....#", "...##"]

big_input = [
    ".#..##.###...#######",
    "##.############..##.",
    ".#.######.########.#",
    ".###.#######.####.#.",
    "#####.##.#.##.###.##",
    "..#####..#.#########",
    "####################",
    "#.####....###.#.#.##",
    "##.#################",
    "#####.##.###..####..",
    "..######..##.#######",
    "####.##.####...##..#",
    ".#####..#.######.###",
    "##...#.##########...",
    "#.##########.#######",
    ".####.#.###.###.#.##",
    "....##.##.###..#####",
    ".#.#.###########.###",
    "#.#.#.#####.####.###",
    "###.##.####.##.#..##",
]

stars = {(4, 4), (1, 2), (4, 0), (3, 4), (4, 3), (4, 2), (0, 2), (2, 2), (1, 0), (3, 2)}


def test_find_angle_from_vertical():
    # assert find_angle_from_vertical((0,0), (-1,0)) < find_angle_from_vertical((0,0), (0,-1))
    assert find_angle_from_vertical((0, 0), (1, 0)) < find_angle_from_vertical(
        (0, 0), (0, 1)
    )
    assert find_angle_from_vertical((0, 0), (0, 1)) < find_angle_from_vertical(
        (0, 0), (-1, 0)
    )


def test_is_colinear():
    assert is_colinear((0, 0), (1, 1), (2, 2)) == True
    assert is_colinear((0, 0), (1, 2), (2, 2)) == False
    assert is_colinear((3, 0), (3, 4), (3, 2)) == True
    assert is_colinear((0, 0), (3, 2), (6, 4)) == True
    assert is_colinear((0, 0), (-3, -2), (6, 4)) == True


def test_is_between_points():
    assert is_between_points((3, 2), (0, 0), (6, 4)) == True
    assert is_between_points((-3, -2), (0, 0), (6, 4)) == False
    assert is_between_points((0, 0), (1, 2), (2, 2)) == False
    assert is_between_points((3, 2), (3, 0), (3, 4)) == True


def test_find_stars():
    assert find_stars(input) == stars


def test_find_asteroids():
    assert find_asteroids(stars, (3, 4)) == {
        (4, 4),
        (1, 2),
        (4, 0),
        (4, 3),
        (4, 2),
        (0, 2),
        (2, 2),
        (3, 2),
    }
    assert len(find_asteroids(find_stars(big_input), (11, 13))) == 210


def test_destroy_asteroids():
    assert destroy_asteroids(find_stars(big_input), (11, 13), 200) == 802


@pytest.mark.parametrize(
    "str_map, best_asteroid, num_detectables",
    [
        ([".#..#", ".....", "#####", "....#", "...##",], (3, 4), 8),
        (
            [
                "......#.#.",
                "#..#.#....",
                "..#######.",
                ".#.#.###..",
                ".#..#.....",
                "..#....#.#",
                "#..#....#.",
                ".##.#..###",
                "##...#..#.",
                ".#....####",
            ],
            (5, 8),
            33,
        ),
        (
            [
                "#.#...#.#.",
                ".###....#.",
                ".#....#...",
                "##.#.#.#.#",
                "....#.#.#.",
                ".##..###.#",
                "..#...##..",
                "..##....##",
                "......#...",
                ".####.###.",
            ],
            (1, 2),
            35,
        ),
        (
            [
                ".#..#..###",
                "####.###.#",
                "....###.#.",
                "..###.##.#",
                "##.##.#.#.",
                "....###..#",
                "..#.#..#.#",
                "#..#.#.###",
                ".##...##.#",
                ".....#.#..",
            ],
            (6, 3),
            41,
        ),
        (
            [
                ".#..##.###...#######",
                "##.############..##.",
                ".#.######.########.#",
                ".###.#######.####.#.",
                "#####.##.#.##.###.##",
                "..#####..#.#########",
                "####################",
                "#.####....###.#.#.##",
                "##.#################",
                "#####.##.###..####..",
                "..######..##.#######",
                "####.##.####...##..#",
                ".#####..#.######.###",
                "##...#.##########...",
                "#.##########.#######",
                ".####.#.###.###.#.##",
                "....##.##.###..#####",
                ".#.#.###########.###",
                "#.#.#.#####.####.###",
                "###.##.####.##.#..##",
            ],
            (11, 13),
            210,
        ),
    ],
)
def test_detectable_asteroids(str_map, best_asteroid, num_detectables):
    assert find_most_asteroids(find_stars(str_map)) == (best_asteroid, num_detectables)


def test_solve():
    assert solve("data/day10.txt") == (267, 1309)
