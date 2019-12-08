from aoc.day8 import (
    find_layers,
    find_layer_with_fewest,
    convert_to_pixels,
    one_layer_array,
    solve,
)

layers = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 0, 1, 2]]
layers2 = [[0, 2, 2, 2], [1, 1, 2, 2], [2, 2, 1, 2], [0, 0, 0, 0]]


def test_find_layers():
    assert (
        find_layers(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "1", "2"], 2, 3)
        == layers
    )


def test_find_layer_with_fewest():
    assert find_layer_with_fewest(layers, 0) == 0


def test_convert_to_pixels():
    assert convert_to_pixels(layers2) == [0, 1, 1, 0]


def test_one_layer_array():
    assert one_layer_array([1, 0, 0, 1, 1, 1], 3) == [[1, 0, 0], [1, 1, 1]]


def test_solve():
    assert solve("data/day8.txt") == (
        1905,
        [
            [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        ],
    )
