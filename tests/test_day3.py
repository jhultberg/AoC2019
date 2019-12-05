from aoc.day3 import closest_distance, shortest_distance, solve


def test_closest_distance():
    assert (
        closest_distance(
            [
                ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
                ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"],
            ]
        )
        == 159
    )
    assert (
        closest_distance(
            [
                [
                    "R98",
                    "U47",
                    "R26",
                    "D63",
                    "R33",
                    "U87",
                    "L62",
                    "D20",
                    "R33",
                    "U53",
                    "R51",
                ],
                ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"],
            ]
        )
        == 135
    )


def test_closest_distance():
    assert (
        shortest_distance(
            [
                ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
                ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"],
            ]
        )
        == 610
    )
    assert (
        shortest_distance(
            [
                [
                    "R98",
                    "U47",
                    "R26",
                    "D63",
                    "R33",
                    "U87",
                    "L62",
                    "D20",
                    "R33",
                    "U53",
                    "R51",
                ],
                ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"],
            ]
        )
        == 410
    )


def test_solve():
    assert solve("data/day3.txt") == (375, 14746)
