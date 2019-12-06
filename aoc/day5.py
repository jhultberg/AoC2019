OP_ADD = "01"
OP_MUL = "02"
OP_INPUT = "03"
OP_OUTPUT = "04"
OP_JUMP_IF_TRUE = "05"
OP_JUMP_IF_FALSE = "06"
OP_LT = "07"
OP_EQ = "08"
OP_EXIT = "99"


class Program:
    def __init__(self, program):
        self.ptr = 0
        self.program = list(program)

    def read(self, immediate=False):
        value = self.program[self.ptr]
        self.ptr += 1
        if not immediate:
            return value
        else:
            return self.program[value]

    def set_pc(self, position):
        self.ptr = position

    def set(self, idx, value, immediate=False):
        if not immediate:
            self.program[idx] = value
        else:
            self.program[self.program[idx]] = value


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


def calc_diagnostics(input_data, input_val):
    program = list(input_data)
    position = 0
    output = 0
    while True:
        instruction = program[position]
        instruction = str(instruction).zfill(5)
        opcode = instruction[3:]

        if opcode == OP_ADD:
            add(program, find_data_three_values(program, position, instruction))
            position += 4
        elif opcode == OP_MUL:
            mul(program, find_data_three_values(program, position, instruction))
            position += 4
        elif opcode == OP_INPUT:
            write(program, program[position + 1], input_val)
            position += 2
        elif opcode == OP_OUTPUT:
            output = find_data_one_value(program, position, instruction)[0]
            position += 2
        elif opcode == OP_JUMP_IF_TRUE:
            values = find_data_two_values(program, position, instruction)
            if values[0] != 0:
                position = values[1]
            else:
                position += 3
        elif opcode == OP_JUMP_IF_FALSE:
            values = find_data_two_values(program, position, instruction)
            if values[0] == 0:
                position = values[1]
            else:
                position += 3
        elif opcode == OP_LT:
            less_than(program, find_data_three_values(program, position, instruction))
            position += 4
        elif opcode == OP_EQ:
            equal(program, find_data_three_values(program, position, instruction))
            position += 4
        elif opcode == OP_EXIT:
            return output
        else:
            raise ValueError("Unexpected OP-code")


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    data = []
    for instruction in input:
        data.append(int(instruction))

    a = calc_diagnostics(data, 1)
    b = calc_diagnostics(data, 5)
    return (a, b)
