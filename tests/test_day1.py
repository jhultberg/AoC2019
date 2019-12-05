from aoc.day1 import calc_sum, recursive_calc_sum, solve


def test_calc_sum():
    assert calc_sum(1969) == 654
    assert calc_sum(100756) == 33583


def test_recursive_calc_sum():
    assert recursive_calc_sum(1969, 0) == 966
    assert recursive_calc_sum(100756, 0) == 50346


def test_solve():
    assert solve("data/day1.txt") == (3412496, 5115845)
