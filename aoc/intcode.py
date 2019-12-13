from collections import defaultdict, deque

OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LT = 7
OP_EQ = 8
OP_REL_BASE = 9
OP_EXIT = 99


class Computer:
    def __init__(self, program, instructions):
        self.program = defaultdict(int, enumerate(program))
        self.instructions = iter(instructions)
        self.position = 0
        self.done = False
        self.relative_base = 0

    def write(self, pos, val):
        self.program[pos] = val

    def get_output_param(self, mode):
        if mode == 0:
            val = self.program[self.position]
        elif mode == 1:
            raise ValueError("Output cannot be immediate mode")
        elif mode == 2:
            val = self.program[self.position] + self.relative_base
        else:
            raise ValueError(f"Unknown mode: {mode}")

        self.position += 1
        return val

    def get_input_param(self, mode):
        if mode == 0:
            val = self.program[self.program[self.position]]
        elif mode == 1:
            val = self.program[self.position]
        elif mode == 2:
            val = self.program[self.program[self.position] + self.relative_base]
        else:
            raise ValueError(f"Unknown mode: {mode}")

        self.position += 1
        return val

    def mul(self, modes):
        left = self.get_input_param(modes[0])
        right = self.get_input_param(modes[1])
        position = self.get_output_param(modes[2])
        self.write(position, left * right)

    def add(self, modes):
        left = self.get_input_param(modes[0])
        right = self.get_input_param(modes[1])
        position = self.get_output_param(modes[2])
        self.write(position, left + right)

    def less_than(self, modes):
        left = self.get_input_param(modes[0])
        right = self.get_input_param(modes[1])
        position = self.get_output_param(modes[2])
        if left < right:
            self.write(position, 1)
        else:
            self.write(position, 0)

    def equal(self, modes):
        left = self.get_input_param(modes[0])
        right = self.get_input_param(modes[1])
        position = self.get_output_param(modes[2])
        if left == right:
            self.write(position, 1)
        else:
            self.write(position, 0)

    def set_rel_base(self, modes):
        value = self.get_input_param(modes[0])
        self.relative_base += value

    def jump_if_true(self, modes):
        cond = self.get_input_param(modes[0])
        jump_pos = self.get_input_param(modes[1])

        if cond != 0:
            self.position = jump_pos

    def jump_if_false(self, modes):
        cond = self.get_input_param(modes[0])
        jump_pos = self.get_input_param(modes[1])

        if cond == 0:
            self.position = jump_pos

    def input(self, modes):
        position = self.get_output_param(modes[0])
        self.write(position, next(self.instructions))


def get_param_modes(instruction):
    modes = defaultdict(int)
    for i, mode in enumerate(reversed(str(instruction)[:-2])):
        modes[i] = int(mode)
    return modes


def run(program, input=deque()):
    computer = Computer(program, input)
    while True:
        instruction = computer.get_input_param(1)
        opcode = instruction % 100
        modes = get_param_modes(instruction)

        if opcode == OP_ADD:
            computer.add(modes)
        elif opcode == OP_MUL:
            computer.mul(modes)
        elif opcode == OP_INPUT:
            computer.input(modes)
        elif opcode == OP_OUTPUT:
            yield computer.get_input_param(modes[0])
        elif opcode == OP_JUMP_IF_TRUE:
            computer.jump_if_true(modes)
        elif opcode == OP_JUMP_IF_FALSE:
            computer.jump_if_false(modes)
        elif opcode == OP_LT:
            computer.less_than(modes)
        elif opcode == OP_EQ:
            computer.equal(modes)
        elif opcode == OP_REL_BASE:
            computer.set_rel_base(modes)
        elif opcode == OP_EXIT:
            computer.done = True
            return
        else:
            raise ValueError(f"Unexpected OP-code: {opcode}")
