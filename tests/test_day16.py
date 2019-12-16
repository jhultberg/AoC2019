from aoc.day16 import calc_one_phase, fft, real_fft, solve


def test_calc_one_phase():
    assert calc_one_phase("12345678") == "48226158"
    assert calc_one_phase("48226158") == "34040438"
    assert calc_one_phase("34040438") == "03415518"
    assert calc_one_phase("03415518") == "01029498"


def test_fft():
    assert fft("80871224585914546619083218645595", 100) == 24176176


def test_real_fft():
    assert real_fft("03036732577212944063491565474664", 100) == 84462026


def test_solve():
    assert solve("data/day16.txt") == (82525123, 49476260)
