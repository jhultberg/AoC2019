OP_ADD = "01"
OP_MUL = "02"
OP_INPUT = "03"
OP_OUTPUT = "04"
OP_JUMP_IF_TRUE = "05"
OP_JUMP_IF_FALSE = "06"
OP_LT = "07"
OP_EQ = "08"
OP_EXIT = "99"


def extract_value(array, instruction):
    if instruction[0] == "0":
        return array[instruction[1]]
    if instruction[0] == "1":
        return instruction[1]


def mul(array, values):
    array[values[2]] = values[0] * values[1]


def add(array, values):
    array[values[2]] = values[0] + values[1]


def write(array, value, input_val):
    array[value] = input_val


def less_than(array, value):
    if value[0] < value[1]:
        array[value[2]] = 1
    else:
        array[value[2]] = 0


def equal(array, value):
    if value[0] == value[1]:
        array[value[2]] = 1
    else:
        array[value[2]] = 0


def calc(input_data, input_val):
    array = list(input_data)
    position = 0
    output = 0
    while True:
        instruction = array[position]
        instruction = str(instruction).zfill(5)
        opcode = instruction[3:]
        values = []
        if opcode == OP_ADD or opcode == OP_MUL or opcode == OP_LT or opcode == OP_EQ:
            first_mode = instruction[2]
            second_mode = instruction[1]
            first = array[position + 1]
            second = array[position + 2]
            third = array[position + 3]
            values = [
                extract_value(array, (first_mode, first)),
                extract_value(array, (second_mode, second)),
                third,
            ]
            position += 4
        elif opcode == OP_INPUT:
            write(array, array[position + 1], input_val)
            position += 2
        elif opcode == OP_OUTPUT:
            first_mode = instruction[2]
            first = array[position + 1]
            values = [extract_value(array, (first_mode, first))]
            position += 2
        elif opcode == OP_JUMP_IF_TRUE or opcode == OP_JUMP_IF_FALSE:
            first_mode = instruction[2]
            second_mode = instruction[1]
            first = array[position + 1]
            second = array[position + 2]
            values = [
                extract_value(array, (first_mode, first)),
                extract_value(array, (second_mode, second)),
            ]
        elif opcode == OP_EXIT:
            return output
        else:
            raise ValueError("Unexpected OP-code")

        if opcode == OP_ADD:
            add(array, values)
        elif opcode == OP_MUL:
            mul(array, values)
        elif opcode == OP_INPUT:
            continue
        elif opcode == OP_OUTPUT:
            output = values[0]
        elif opcode == OP_JUMP_IF_TRUE:
            if values[0] != 0:
                position = values[1]
            else:
                position += 3
        elif opcode == OP_JUMP_IF_FALSE:
            if values[0] == 0:
                position = values[1]
            else:
                position += 3
        elif opcode == OP_LT:
            less_than(array, values)
        elif opcode == OP_EQ:
            equal(array, values)
        else:
            raise ValueError("Unexpected OP-code")


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    data = []
    for instruction in input:
        data.append(int(instruction))

    a = calc(data, 1)
    b = calc(data, 5)
    return (a, b)
