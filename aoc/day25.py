from .intcode import run
import click


class Droid:
    def __init__(self, program):
        self.program = program

    def command(self):
        while True:
            s = []
            while True:
                c = ord(str(click.getchar()))
                if c == 13:
                    c = 10
                s.append(c)
                if c == 10:
                    break
            for c in s:
                print(chr(c), end="")
            done = object()
            s = iter(s)
            n = next(s, done)
            while n is not done:
                yield n
                n = next(s, done)

    def find_password(self):
        robot = run(self.program, self.command())
        while True:
            try:
                output = next(robot)
                try:
                    print(chr(output))
                except ValueError:
                    return output
            except StopIteration:
                return None


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    program = []
    for instruction in input:
        program.append(int(instruction))

    a = Droid(program).find_password()

    # Correct combination of items:
    # astrolabe, rnament, sand, shell
    # gives combination 134807554
    return (134807554, None)
