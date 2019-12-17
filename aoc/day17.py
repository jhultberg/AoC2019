from .intcode import run
from collections import defaultdict
from operator import itemgetter
from itertools import count
import time


def ascii_to_direction(ascii_val):
    if ascii_val == 94:
        # UP
        return 0
    elif ascii_val == 62:
        # RIGHT
        return 1
    elif ascii_val == 118:
        # SOUTH
        return 2
    elif ascii_val == 60:
        # LEFT
        return 3
    else:
        raise ValueError(f"Unexpected ascii direction: {ascii_val}")


class Robot:

    dir_to_coord = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}

    def __init__(self, x, y, direction):
        self.position = (x, y)
        self.direction = ascii_to_direction(direction)
        self.dust = 0

    def can_step(self, scaffold):
        return (
            tuple(
                a + b for a, b in zip(self.position, self.dir_to_coord[self.direction])
            )
            in scaffold
        )

    def take_step(self):
        self.position = tuple(
            a + b for a, b in zip(self.position, self.dir_to_coord[self.direction])
        )

    def peek_position(self):
        return tuple(
            a + b for a, b in zip(self.position, self.dir_to_coord[self.direction])
        )

    def turn_right(self):
        self.direction += 1
        self.direction %= 4


class Vacuum:
    def __init__(self, program):
        self.program = program
        self.board = defaultdict(int)
        self.robot = None
        self.scaffold = []

    def sum_alignment_parameters(self):
        max_x = max(self.board, key=itemgetter(0))[0]
        max_y = max(self.board, key=itemgetter(1))[1]

        tot = 0
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                # need special for borders
                if x == 0 or y == 0 or x == max_x or y == max_y:
                    continue
                if (
                    self.board[(x, y)] == 35
                    and self.board[(x + 1, y)] == 35
                    and self.board[(x - 1, y)] == 35
                    and self.board[(x, y + 1)] == 35
                    and self.board[(x, y - 1)] == 35
                ):
                    tot += x * y

        return tot

    def render(self):
        time.sleep(0.01)
        max_x = max(self.board, key=itemgetter(0))[0] + 1
        max_y = max(self.board, key=itemgetter(1))[1] + 1
        min_x = min(self.board, key=itemgetter(0))[0]
        min_y = min(self.board, key=itemgetter(1))[1]
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                coord = self.board[(x, y)]
                print(chr(coord), end="")
            print()
        print()

    def collect_dust(self):
        route = self.find_route()

        A = route[:4]
        B = route[4:9]
        C = route[18:21]

        main = "A,B,A,B,C,C,B,A,B,C\n"
        main_ascii = [ord(c) for c in main]

        instructions = iter(
            main_ascii + to_ascii(A) + to_ascii(B) + to_ascii(C) + [ord("n"), ord("\n")]
        )

        while True:
            yield next(instructions)

    def alignment_parameters(self, takes_input=False):
        if takes_input:
            self.program[0] = 2
            robot = run(self.program, self.collect_dust())
        else:
            robot = run(self.program, [])
        x = 0
        y = 0
        for i in count():
            try:
                output = next(robot)
                if output == 10:
                    x = 0
                    y += 1
                elif output == 35:
                    self.board[(x, y)] = output
                    x += 1
                    self.scaffold.append((x, y))
                elif output == 46:
                    self.board[(x, y)] = output
                    x += 1

                elif output == 94 or output == 62 or output == 118 or output == 60:
                    self.robot = Robot(x, y, output)
                    self.board[(x, y)] = output
                    x += 1
                else:
                    print(chr(output))
                    self.robot.dust = output
            except StopIteration:
                self.render()
                return (self.sum_alignment_parameters(), self.robot.dust)

    def find_route(self):
        visited = set()
        route = []

        prev_dir = self.robot.direction
        visited.add(self.robot.position)

        for _ in range(4):
            self.robot.turn_right()
            if self.robot.can_step(self.scaffold):
                curr_dir = find_left_right_from_dirs(prev_dir, self.robot.direction)
                break

        count = 1
        while True:
            if self.robot.can_step(self.scaffold):
                self.robot.take_step()
                visited.add(self.robot.position)
                count += 1
                continue

            route.append((count, curr_dir))
            count = 1
            can_continue = False
            prev_dir = self.robot.direction

            for _ in range(4):
                self.robot.turn_right()
                if (
                    self.robot.can_step(self.scaffold)
                    and self.robot.peek_position() not in visited
                ):
                    self.robot.take_step()
                    visited.add(self.robot.position)
                    can_continue = True
                    curr_dir = find_left_right_from_dirs(prev_dir, self.robot.direction)
                    break
            if not can_continue:
                return route


def to_ascii(data):
    in_ascii = []
    for val in data:
        num = str(val[0])
        in_ascii.append(ord(str(val[1])))
        in_ascii.append(ord(","))
        for digit in num:
            in_ascii.append(ord(digit))
        in_ascii.append(ord(","))

    in_ascii.pop()
    in_ascii.append(ord("\n"))
    return in_ascii


def find_left_right_from_dirs(prev_dir, new_dir):
    if prev_dir == 0 and new_dir == 1:
        return "R"
    elif prev_dir == 0 and new_dir == 3:
        return "L"
    elif prev_dir == 1 and new_dir == 2:
        return "R"
    elif prev_dir == 1 and new_dir == 0:
        return "L"
    elif prev_dir == 2 and new_dir == 3:
        return "R"
    elif prev_dir == 2 and new_dir == 1:
        return "L"
    elif prev_dir == 3 and new_dir == 0:
        return "R"
    elif prev_dir == 3 and new_dir == 2:
        return "L"
    else:
        raise ValueError(f"Unexpected turn, prev_dir {prev_dir}, new_dir {new_dir}")


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    input_data = []
    for instruction in input:
        input_data.append(int(instruction))

    a = Vacuum(list(input_data)).alignment_parameters()[0]
    b = Vacuum(list(input_data)).alignment_parameters(takes_input=True)[1]

    return (a, b)
