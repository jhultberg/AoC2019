from .intcode import run
from collections import deque
from operator import itemgetter


class Position:

    DIR_UP = 0
    DIR_LEFT = 1
    DIR_DOWN = 2
    DIR_RIGHT = 3

    def __init__(self, x=0, y=0, direction=DIR_UP):
        self.x_pos = x
        self.y_pos = y
        self.direction = direction

    def turn_left(self):
        if self.direction == self.DIR_UP:
            self.direction = self.DIR_LEFT
            self.x_pos = self.x_pos - 1
        elif self.direction == self.DIR_LEFT:
            self.direction = self.DIR_DOWN
            self.y_pos = self.y_pos - 1
        elif self.direction == self.DIR_DOWN:
            self.direction = self.DIR_RIGHT
            self.x_pos = self.x_pos + 1
        elif self.direction == self.DIR_RIGHT:
            self.direction = self.DIR_UP
            self.y_pos = self.y_pos + 1

    def turn_right(self):
        if self.direction == self.DIR_UP:
            self.direction = self.DIR_RIGHT
            self.x_pos = self.x_pos + 1
        elif self.direction == self.DIR_RIGHT:
            self.direction = self.DIR_DOWN
            self.y_pos = self.y_pos - 1
        elif self.direction == self.DIR_DOWN:
            self.direction = self.DIR_LEFT
            self.x_pos = self.x_pos - 1
        elif self.direction == self.DIR_LEFT:
            self.direction = self.DIR_UP
            self.y_pos = self.y_pos + 1

    def get_coordinate(self):
        return (self.x_pos, self.y_pos)


def painting_robot(program, start_on_white=False):
    robot_instructions = deque()
    robot = run(program, robot_instructions)
    robot_position = Position()

    painted_squares = set()
    white = set()
    if start_on_white:
        white.add(robot_position.get_coordinate())

    while True:
        curr_coord = robot_position.get_coordinate()
        if curr_coord in white:
            robot_instructions.append(1)
        else:
            robot_instructions.append(0)
        try:
            color = next(robot)
            turn = next(robot)

            if color == 0:
                if curr_coord in white:
                    white.remove(curr_coord)
            elif color == 1:
                white.add(curr_coord)
            else:
                raise ValueError(f"Unexpected color: {color}")
            painted_squares.add(curr_coord)

            if turn == 0:
                robot_position.turn_left()
            elif turn == 1:
                robot_position.turn_right()
            else:
                raise ValueError(f"Unexpected way to turn: {turn}")

        except StopIteration:
            return (painted_squares, white)


def render(coordinates):
    cl = list(coordinates)
    max_x = max(cl, key=itemgetter(0))[0] + 1
    max_y = max(cl, key=itemgetter(1))[1] + 1
    min_x = min(cl, key=itemgetter(0))[0]
    min_y = min(cl, key=itemgetter(1))[1]

    for y in reversed(range(min_y, max_y)):
        for x in range(min_x, max_x):
            if (x, y) in coordinates:
                print("#", end="")
            else:
                print(" ", end="")
        print()

    return None


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    input_data = []
    for instruction in input:
        input_data.append(int(instruction))

    a = len(painting_robot(input_data)[0])
    b = render(painting_robot(input_data, start_on_white=True)[1])

    return (a, b)
