from aoc.day4 import is_valid_password, is_valid_password_2, solve


def test_is_valid_password():
    assert is_valid_password(111111) == True
    assert is_valid_password(223450) == False
    assert is_valid_password(123789) == False


def test_is_valid_password_2():
    assert is_valid_password_2(112233) == True
    assert is_valid_password_2(123444) == False
    assert is_valid_password_2(111233) == True
    assert is_valid_password_2(111122) == True


def test_solve():
    assert solve(165432, 707912) == (1716, 1163)
