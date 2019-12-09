from .intcode import run


def last(it):
    out = None
    for i in it:
        out = i
    return out


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    data = []
    for instruction in input:
        data.append(int(instruction))

    a = last(run(data, [1]))
    b = next(run(data, [5]))
    return (a, b)
