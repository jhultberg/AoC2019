from .intcode import run


class SpringDroid:
    def __init__(self, program):
        self.program = program

    def walk(self, part):
        if part == "a":
            instructions = [
                "NOT A J",  # !A
                "NOT B T",  # !B
                "OR T J",  # !A or !B
                "NOT C T",  # !C
                "OR T J",  # !A or !B or !C
                "AND D J",  # (!A or !B or !C) & D
                "WALK",
            ]
        elif part == "b":
            instructions = [
                "NOT A J",  # !A
                "AND D J",  # !A & D
                "NOT B T",  # !B
                "AND D T",  # !B & D
                "OR T J",  # (!A & D) or (!B & D)
                "NOT C T",  # !C
                "AND D T",  # !C & D
                "AND H T",  # !C & D & H
                "OR T J ",  # (!C & D & H) or (!A & D) or (!B & D)
                "RUN",
            ]
        instructions = iter(to_ascii(instructions))

        while True:
            yield next(instructions)

    def map_damage(self, part):
        robot = run(self.program, self.walk(part))
        while True:
            try:
                output = next(robot)
                try:
                    print(chr(output))
                except ValueError:
                    return output
            except StopIteration:
                return None


def to_ascii(instructions):

    for instruction in instructions:
        for val in instruction:
            yield ord(str(val))
        yield ord("\n")


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    program = []
    for instruction in input:
        program.append(int(instruction))

    a = SpringDroid(list(program)).map_damage("a")
    b = SpringDroid(list(program)).map_damage("b")

    return (a, b)
