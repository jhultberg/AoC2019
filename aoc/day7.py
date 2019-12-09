import itertools
from .intcode import run
from collections import deque


def calc_thruster(program, input, settings):
    prev_output = input
    for setting in settings:
        prev_output = next(run(program, [setting, prev_output]))
    return prev_output


def calc_with_feedback(program, settings):
    deque_a = deque([settings[0], 0])
    deque_b = deque([settings[1]])
    deque_c = deque([settings[2]])
    deque_d = deque([settings[3]])
    deque_e = deque([settings[4]])
    amplifier_a = run(program, deque_a)
    amplifier_b = run(program, deque_b)
    amplifier_c = run(program, deque_c)
    amplifier_d = run(program, deque_d)
    amplifier_e = run(program, deque_e)
    while True:
        deque_b.append(next(amplifier_a, None))
        deque_c.append(next(amplifier_b, None))
        deque_d.append(next(amplifier_c, None))
        deque_e.append(next(amplifier_d, None))
        try:
            deque_a.append(next(amplifier_e))
        except StopIteration:
            return deque_a.popleft()


def calc_max_thrust(program, with_feedback=False):
    if with_feedback:
        phases = range(5, 10)
    else:
        phases = range(5)

    max_signal = 0
    for setting in itertools.permutations(phases):
        if with_feedback:
            thrust_signal = calc_with_feedback(program, setting)
        else:
            print(setting, setting[0])
            thrust_signal = calc_thruster(program, 0, setting)
        if thrust_signal > max_signal:
            max_signal = thrust_signal
    return max_signal


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    input_data = []
    for instruction in input:
        input_data.append(int(instruction))

    a = calc_max_thrust(input_data)
    b = calc_max_thrust(input_data, with_feedback=True)
    return (a, b)
