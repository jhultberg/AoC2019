from .intcode import run


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    input_data = []
    for instruction in input:
        input_data.append(int(instruction))

    a = next(run(input_data, [1]))
    b = next(run(input_data, [2]))

    return (a, b)
