from .intcode import run
from itertools import count
from operator import itemgetter


def render(area):
    max_x = max(area, key=itemgetter(0))[0]
    max_y = max(area, key=itemgetter(1))[1]
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            coord = area[(x, y)]
            if coord == 1:
                print("#", end="")
            elif coord == 0:
                print(".", end="")
        print(y)
    print()


def fit_santa(program, size):
    y = size
    for x in count():
        if query_pos(program, x, y) == 1:
            initial_x = x
            break

    history = [None] * size

    while True:
        current = query_row(program, initial_x, y)

        if history[-1]:
            if current[0] + size == history[(y + 1) % size][0]:
                return current[0] * 10_000 + history[(y + 1) % size][1]

        history[y % size] = (current[1], y)
        initial_x = current[0]

        y += 1


def query_pos(program, x, y):
    return next(run(program, [x, y]))


def query_row(program, start_x, y):
    if query_pos(program, start_x, y) == 0:
        start_x += 1
    x = start_x
    while query_pos(program, x, y) == 1:
        x += 1

    return (start_x, x)


def query_area(program, size):
    area = {}
    for y in range(size):
        for x in range(size):
            area[(x, y)] = query_pos(program, x, y)
    render(area)
    return area


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    program = []
    for instruction in input:
        program.append(int(instruction))

    a = sum(query_area(program, 50).values())
    b = fit_santa(program, 100)

    return (a, b)
