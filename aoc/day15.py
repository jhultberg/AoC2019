from .intcode import run
from collections import defaultdict, deque
from itertools import count
from operator import itemgetter
import time


class Droid:

    DIR_NORTH = 1
    DIR_SOUTH = 2
    DIR_WEST = 3
    DIR_EAST = 4

    def __init__(self, program):
        self.program = program
        self.board = defaultdict(int)
        self.position = (0, 0)
        self.oxygen = None
        self.direction = self.DIR_NORTH
        self.route = []
        self.visited = set()

        self.board[(0, 0)] = 1

    def render(self, i):
        time.sleep(0.01)
        max_x = max(self.board, key=itemgetter(0))[0] + 1
        max_y = max(self.board, key=itemgetter(1))[1] + 1
        min_x = min(self.board, key=itemgetter(0))[0]
        min_y = min(self.board, key=itemgetter(1))[1]
        for y in reversed(range(min_y, max_y)):
            for x in range(min_x, max_x):
                if (x, y) not in self.board:
                    print(" ", end="")
                    continue
                if (x, y) == self.position:
                    print("X", end="")
                    continue

                coord = self.board[(x, y)]
                if coord == 0:
                    print("#", end="")
                if coord == 1:
                    print(".", end="")
                if coord == 2:
                    print("O", end="")
            print()
        print()
        print('iteration', i)
        print('route', self.route)
        print('oxygen', self.oxygen)

    def update_position(self):
        self.position = self.find_next_position(self.direction)
        self.route.append(self.direction)
        self.visited.add(self.position)

    def find_next_position(self, direction):
        if direction == self.DIR_NORTH:
            return (self.position[0], self.position[1] + 1)
        elif direction == self.DIR_SOUTH:
            return (self.position[0], self.position[1] - 1)
        elif direction == self.DIR_EAST:
            return (self.position[0] + 1, self.position[1])
        elif direction == self.DIR_WEST:
            return (self.position[0] - 1, self.position[1])

    def found_oxygen(self):
        self.oxygen = self.position
        self.board[self.position] = 2

    def turn_left(self):
        if self.direction == self.DIR_NORTH:
            self.direction = self.DIR_WEST
        elif self.direction == self.DIR_WEST:
            self.direction = self.DIR_SOUTH
        elif self.direction == self.DIR_SOUTH:
            self.direction = self.DIR_EAST
        elif self.direction == self.DIR_EAST:
            self.direction = self.DIR_NORTH

    def turn_right(self):
        self.turn_left()
        self.turn_left()
        self.turn_left()


    def inverse_direction(self, direction):
        if direction == self.DIR_SOUTH:
            return self.DIR_NORTH
        elif direction == self.DIR_NORTH:
            return self.DIR_SOUTH
        elif direction == self.DIR_WEST:
            return self.DIR_EAST
        elif direction == self.DIR_EAST:
            return self.DIR_WEST

    def backtrack(self):
        print('back', self.route)
        prev = self.route.pop()
        self.direction = self.inverse_direction(prev)
        self.update_position()
        print('dir', self.direction)
        print('posiiotn', self.position)
        input()
        self.route.pop()


    def movements(self):
        while True:
            yield self.direction

    def explore(self):
        droid = run(self.program, self.movements())
        for i in count():
            try:
                status_code = next(droid)
                if status_code == 0:
                    # wall
                    self.board[self.find_next_position(self.direction)] = 0
                    self.visited.add(self.find_next_position(self.direction))
                elif status_code == 1:
                    # moved
                    # update position
                    self.update_position()
                    self.board[self.position] = 1
                elif status_code == 2:
                    # found oxygen
                    self.update_position()
                    self.found_oxygen()
                else:
                    raise ValueError(f"Unexpected game instruction: {output}")

                if self.find_next_position(self.direction) not in self.visited:
                    continue
                self.turn_left()
                if self.find_next_position(self.direction) not in self.visited:
                    continue
                self.turn_left()
                if self.find_next_position(self.direction) not in self.visited:
                    continue
                self.turn_left()
                if self.find_next_position(self.direction) not in self.visited:
                    continue
                if self.route:
                    self.backtrack()
                else:
                    return self.oxygen


                self.render(i)
            except StopIteration:
                print("stop")
                self.render(i)
                return None

    def shortest_route(self):
        pass

    # BFS


def find_oxygen(program):
    a = Droid(program).explore()
    return a


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    input_data = []
    for instruction in input:
        input_data.append(int(instruction))

    a = find_oxygen(input_data)

    return (a, None)
