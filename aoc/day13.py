from .intcode import run
from collections import defaultdict, deque
from operator import itemgetter
from itertools import count
import time


class Game:
    def __init__(self, program):
        self.program = program
        self.board = defaultdict()
        self.ball = (-1, -1)
        self.paddle = (-1, -1)
        self.score = 0

    def render(self):
        time.sleep(0.01)
        max_x = max(self.board, key=itemgetter(0))[0] + 1
        max_y = max(self.board, key=itemgetter(1))[1] + 1
        min_x = min(self.board, key=itemgetter(0))[0]
        min_y = min(self.board, key=itemgetter(1))[1]
        for y in reversed(range(min_y, max_y)):
            for x in range(min_x, max_x):
                coord = self.board[(x, y)]
                if coord == 0:
                    print(" ", end="")
                if coord == 1:
                    print("#", end="")
                if coord == 2:
                    print("x", end="")
                if coord == 3:
                    print("_", end="")
                if coord == 4:
                    print("O", end="")
            print()
        print()

    def joystick(self):
        while True:
            # self.render()
            if self.ball[0] == self.paddle[0]:
                yield 0
            elif self.ball[0] < self.paddle[0]:
                yield -1
            elif self.ball[0] > self.paddle[0]:
                yield 1

    def play_game(self):
        game = run(self.program, self.joystick())
        for i in count():
            try:
                x = next(game)
                y = next(game)
                output = next(game)
                if x == -1 and y == 0:
                    self.score = output
                elif output == 0:
                    self.board[(x, y)] = 0
                elif output == 1:
                    self.board[(x, y)] = 1
                elif output == 2:
                    self.board[(x, y)] = 2
                elif output == 3:
                    self.board[(x, y)] = 3
                    self.paddle = (x, y)
                elif output == 4:
                    self.board[(x, y)] = 4
                    self.ball = (x, y)
                else:
                    raise ValueError(f"Unexpected game instruction: {output}")
            except StopIteration:
                return (sum(value == 2 for value in self.board.values()), self.score)


def arcade(program, play_for_free=False):
    if play_for_free:
        program[0] = 2

    a, b = Game(program).play_game()
    return (a, b)


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    input_data = []
    for instruction in input:
        input_data.append(int(instruction))

    a = arcade(input_data)[0]
    b = arcade(input_data, play_for_free=True)[1]

    return (a, b)
