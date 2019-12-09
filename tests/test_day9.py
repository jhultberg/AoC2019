from aoc.day9 import run, solve


def test_boost():
    assert list(
        run([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99])
    ) == [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

    assert len(str(next(run([1102, 34915192, 34915192, 7, 4, 7, 99, 0])))) == 16

    assert list(run([104, 1125899906842624, 99])) == [1125899906842624]
    # assert list(run([109, 1, 201, 1, 1, -1, 4, 0])) == [2]


def test_solve():
    assert solve("data/day9.txt") == (2941952859, 66113)
