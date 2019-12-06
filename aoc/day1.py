import math


def calc_sum(line):
    return math.floor(line / 3) - 2


def recursive_calc_sum(val, total_sum):
    sum = calc_sum(val)
    if sum > 0:
        return recursive_calc_sum(sum, total_sum + sum)
    return int(total_sum)


def solve(path):
    with open(path) as ins:
        a = 0
        b = 0
        for line in ins:
            a += calc_sum(int(line))
            b += recursive_calc_sum(int(line), 0)
    return (a, b)
