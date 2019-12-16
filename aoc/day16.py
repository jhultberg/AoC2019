from itertools import chain, cycle, repeat, islice


def calc_one_phase(input):
    base_pattern = [0, 1, 0, -1]
    result = []
    for i in range(len(input)):
        pattern = cycle(
            list(chain.from_iterable(repeat(x, i + 1) for x in base_pattern))
        )
        next(pattern)
        n = 0
        for digit in input:
            n += int(digit) * next(pattern)
        result.append(abs(n) % 10)
    s = [str(i) for i in result]
    res = "".join(s)
    return res


def fft(input, phases):
    res = input
    for _ in range(phases):
        res = calc_one_phase(res)
    return int("".join([str(x) for x in res[:8]]))


def real_fft(input, phases):
    start_index = int(input[:7])
    total_len = len(input) * 10000
    a = (total_len - start_index) // len(input) + 1
    end_size = a * len(input)
    offset = abs(total_len - start_index - end_size)

    input = list(
        islice(cycle([int(x) for x in input]), offset, total_len - start_index + offset)
    )
    for _ in range(phases):
        output = []
        val = sum(input)
        output.append(val % 10)
        for idx, value in enumerate(input[:-1]):
            val -= value
            output.append(val % 10)
        input = output
    return int("".join([str(x) for x in output[:8]]))


def solve(path):
    with open(path) as f:
        input = f.readlines()
    input = input[0].rstrip()
    a = fft(input, phases=100)
    b = real_fft(input, phases=100)
    return (a, b)
