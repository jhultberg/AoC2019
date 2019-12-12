from aoc.day12 import (
    Moon,
    kin_energy,
    pot_energy,
    simulate,
    find_moons,
    total_energy,
    total_iterations_to_repetition,
    split_dimension,
    solve,
)
from copy import deepcopy

input = [
    "<x=-1, y=0, z=2>",
    "<x=2, y=10, z=-7>",
    "<x=4, y=-8, z=8>",
    "<x=3, y=5, z=-1>",
]

moons = [Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1)]
moons_2 = [Moon(-8, -10, 0), Moon(5, 5, 10), Moon(2, -7, 3), Moon(9, -8, -3)]
moons_after_10 = [
    Moon(2, 1, -3, 3, -2, 1),
    Moon(1, -8, 0, -1, 1, 3),
    Moon(3, -6, 1, 3, 2, -3),
    Moon(2, 0, 4, 1, -1, -1),
]


def test_kin_energy():
    assert kin_energy(moons_after_10[0]) == 6
    assert kin_energy(moons_after_10[1]) == 5
    assert kin_energy(moons_after_10[2]) == 8
    assert kin_energy(moons_after_10[3]) == 3


def test_pot_energy():
    assert pot_energy(moons_after_10[0]) == 6
    assert pot_energy(moons_after_10[1]) == 9
    assert pot_energy(moons_after_10[2]) == 10
    assert pot_energy(moons_after_10[3]) == 6


def test_total_energy():
    assert sum(total_energy(moons_after_10)) == 179


def test_simulate():
    assert sum(total_energy(simulate(deepcopy(moons), 10))) == 179


def test_split_dimension():
    assert list(split_dimension(moons_after_10, "x")) == [
        (2, 3),
        (1, -1),
        (3, 3),
        (2, 1),
    ]
    assert list(split_dimension(moons_after_10, "y")) == [
        (1, -2),
        (-8, 1),
        (-6, 2),
        (0, -1),
    ]
    assert list(split_dimension(moons_after_10, "z")) == [
        (-3, 1),
        (0, 3),
        (1, -3),
        (4, -1),
    ]


def test_total_iterations_to_repetition():
    assert total_iterations_to_repetition(deepcopy(moons)) == 2772
    assert total_iterations_to_repetition(deepcopy(moons_2)) == 4686774924


def test_solve():
    assert solve("data/day12.txt") == (12082, 295693702908636)
