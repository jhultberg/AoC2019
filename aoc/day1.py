import math


def calc_sum(line):
    return math.floor(line / 3) - 2


def recursive_calc_sum(val, total_sum):
    sum = calc_sum(val)
    if sum > 0:
        return recursive_calc_sum(sum, total_sum + sum)
    # print(total_sum)
    return int(total_sum)


def rec_calc(lines):
    sum = 0
    for line in lines:
        sum += recursive_calc_sum(line, 0)
    return sum


assert recursive_calc_sum(1969, 0) == 966
assert recursive_calc_sum(100756, 0) == 50346


def solve(path):
    with open(path) as ins:
        a = 0
        b = 0
        for line in ins:
            a += calc_sum(int(line))
            b += recursive_calc_sum(int(line), 0)
    return (a, b)
