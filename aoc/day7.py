import itertools

OP_ADD = "01"
OP_MUL = "02"
OP_INPUT = "03"
OP_OUTPUT = "04"
OP_JUMP_IF_TRUE = "05"
OP_JUMP_IF_FALSE = "06"
OP_LT = "07"
OP_EQ = "08"
OP_EXIT = "99"


class DiagnosticData:
    def __init__(self, program, instructions):
        self.program = program
        self.instructions = instructions
        self.position = 0
        self.done = False


def extract_value(program, instruction):
    if instruction[0] == "0":
        return program[instruction[1]]
    if instruction[0] == "1":
        return instruction[1]


def mul(program, values):
    program[values[2]] = values[0] * values[1]


def add(program, values):
    program[values[2]] = values[0] + values[1]


def write(program, value, input_val):
    program[value] = input_val


def less_than(program, value):
    if value[0] < value[1]:
        program[value[2]] = 1
    else:
        program[value[2]] = 0


def equal(program, value):
    if value[0] == value[1]:
        program[value[2]] = 1
    else:
        program[value[2]] = 0


def find_data_three_values(program, position, instructions):
    first_mode = instructions[2]
    second_mode = instructions[1]
    first = program[position + 1]
    second = program[position + 2]
    third = program[position + 3]
    return [
        extract_value(program, (first_mode, first)),
        extract_value(program, (second_mode, second)),
        third,
    ]


def find_data_two_values(program, position, instructions):
    first_mode = instructions[2]
    second_mode = instructions[1]
    first = program[position + 1]
    second = program[position + 2]
    return [
        extract_value(program, (first_mode, first)),
        extract_value(program, (second_mode, second)),
    ]


def find_data_one_value(program, position, instructions):
    first_mode = instructions[2]
    first = program[position + 1]
    return [extract_value(program, (first_mode, first))]


def calc_diagnostics(diagnostic_data):
    program = diagnostic_data.program
    while True:
        instruction = program[diagnostic_data.position]
        instruction = str(instruction).zfill(5)
        opcode = instruction[3:]

        if opcode == OP_ADD:
            add(
                program,
                find_data_three_values(program, diagnostic_data.position, instruction),
            )
            diagnostic_data.position += 4
        elif opcode == OP_MUL:
            mul(
                program,
                find_data_three_values(program, diagnostic_data.position, instruction),
            )
            diagnostic_data.position += 4
        elif opcode == OP_INPUT:
            if not diagnostic_data.instructions:
                return
            else:
                write(
                    program,
                    program[diagnostic_data.position + 1],
                    diagnostic_data.instructions[0],
                )
                diagnostic_data.instructions = diagnostic_data.instructions[1:]
                diagnostic_data.position += 2
        elif opcode == OP_OUTPUT:
            pos = diagnostic_data.position
            diagnostic_data.position += 2
            yield find_data_one_value(program, pos, instruction)[0]
        elif opcode == OP_JUMP_IF_TRUE:
            values = find_data_two_values(
                program, diagnostic_data.position, instruction
            )
            if values[0] != 0:
                diagnostic_data.position = values[1]
            else:
                diagnostic_data.position += 3
        elif opcode == OP_JUMP_IF_FALSE:
            values = find_data_two_values(
                program, diagnostic_data.position, instruction
            )
            if values[0] == 0:
                diagnostic_data.position = values[1]
            else:
                diagnostic_data.position += 3
        elif opcode == OP_LT:
            less_than(
                program,
                find_data_three_values(program, diagnostic_data.position, instruction),
            )
            diagnostic_data.position += 4
        elif opcode == OP_EQ:
            equal(
                program,
                find_data_three_values(program, diagnostic_data.position, instruction),
            )
            diagnostic_data.position += 4
        elif opcode == OP_EXIT:
            diagnostic_data.done = True
            return
        else:
            raise ValueError("Unexpected OP-code")


def calc_thruster(input_data, input, settings):
    if settings == []:
        return input
    data = list(input_data)
    output = calc_diagnostics(DiagnosticData(data, [settings[0], input]))
    return calc_thruster(input_data, next(output), settings[1:])


def calc_with_feedback(data, settings):
    data_a = DiagnosticData(list(data), [settings[0], 0])
    data_b = DiagnosticData(list(data), [settings[1]])
    data_c = DiagnosticData(list(data), [settings[2]])
    data_d = DiagnosticData(list(data), [settings[3]])
    data_e = DiagnosticData(list(data), [settings[4]])
    while True:
        for b in calc_diagnostics(data_a):
            data_b.instructions.append(b)
        for c in calc_diagnostics(data_b):
            data_c.instructions.append(c)
        for d in calc_diagnostics(data_c):
            data_d.instructions.append(d)
        for e in calc_diagnostics(data_d):
            data_e.instructions.append(e)
        for a in calc_diagnostics(data_e):
            data_a.instructions.append(a)
        if data_a.done and data_b.done and data_c.done and data_d.done and data_e.done:
            return data_a.instructions[0]


def calc_max_thrust(input_data, with_feedback):
    if with_feedback:
        phases = list(itertools.permutations(list(range(5, 10))))
    else:
        phases = list(itertools.permutations(list(range(0, 5))))

    max_signal = 0
    for setting in phases:
        data = list(input_data)
        if with_feedback:
            thrust_signal = calc_with_feedback(data, setting)
        else:
            thrust_signal = calc_thruster(data, 0, list(setting))
        if thrust_signal > max_signal:
            max_signal = thrust_signal
    return max_signal


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    input_data = []
    for instruction in input:
        input_data.append(int(instruction))

    a = calc_max_thrust(input_data, False)
    b = calc_max_thrust(input_data, True)
    return (a, b)
