import re


def parse_input(input):
    parsed_program = []
    for row in input:
        if re.match(r"([a-z\s]*) (-?\d*)\n", row):
            inst, number = re.match(r"([a-z\s]*) (-?\d*)\n", row).groups()
        else:
            inst = re.match(r"([a-z\s]*)\n", row)
            inst = inst.group(0)
        if inst == "cut":
            parsed_program.append(("cut", int(number)))
        elif inst == "deal with increment":
            parsed_program.append(("incr", int(number)))
        elif inst == "deal into new stack\n":
            parsed_program.append(("stack", None))
        else:
            raise ValueError(f"Unexpected instruction to parse: {inst}")
    return parsed_program


def k_and_m(program, deck_size):
    m = 0
    k = 1
    for instruction in program:
        if instruction[0] == "cut":
            m -= instruction[1]
        elif instruction[0] == "incr":
            k *= instruction[1]
            m *= instruction[1]
        elif instruction[0] == "stack":
            k *= -1
            m = deck_size - m - 1
        else:
            raise ValueError(f"Unexpected instruction in shuffle2: {instruction[0]}")
    k %= deck_size
    m %= deck_size
    return k, m


def shuffle(program, deck_size, position):
    k, m = k_and_m(program, deck_size)
    return (k * position + m) % deck_size


def lcg(k, m, mod, x, iterations=1):
    if iterations == 1:
        return (k * x + m) % mod

    if iterations < 0:
        k_inv = pow(k, -1, mod)
        k = k_inv
        m = -k * m
        iterations = abs(iterations)

    m = (pow(k, iterations, (k - 1) * mod) - 1) // (k - 1) * m
    k = pow(k, iterations, mod)
    return (k * x + m) % mod


def solve(path):
    with open(path) as f:
        input = f.readlines()

    program = parse_input(input)

    a = shuffle(program, 10007, 2019)

    mega_deck_size = 119_315_717_514_047
    no_shufflings = 101_741_582_076_661

    k, m = k_and_m(program, mega_deck_size)
    b = lcg(k, m, mega_deck_size, 2020, -no_shufflings)

    return (a, b)
