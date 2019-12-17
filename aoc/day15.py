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
        self.direction = self.DIR_WEST
        self.route = []
        self.visited = set()
        #self.droid = maze_tester(self.movements())
        self.droid = run(self.program, self.movements())
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

    def update_position(self):
        self.position = self.find_next_position(self.direction)
        self.route.append(self.direction)
        self.visited.add(self.position)

    def find_next_position(self, direction):
        if direction == self.DIR_NORTH:
            return (self.position[0], self.position[1] - 1)
        elif direction == self.DIR_SOUTH:
            return (self.position[0], self.position[1] + 1)
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
        self.move(self.inverse_direction(self.route.pop()))
        self.position = self.find_next_position(self.direction)
        #input()

    def movements(self):
        while True:
            yield self.direction

    def move(self, cmd):
        self.direction = cmd
        status = next(self.droid)
        return status

    def find_next_direction(self):
        for i in range(1,5):
            if self.find_next_position(i) not in self.visited:
                return i


    def explore(self):
        for i in count():
            try:
                cmd = self.find_next_direction()
                if cmd is None:
                    if not self.route:
                        self.render(i)
                        return self.oxygen
                    self.backtrack()
                    continue

                status_code = self.move(cmd)
                if status_code == 0:
                    self.board[self.find_next_position(self.direction)] = 0
                    self.visited.add(self.find_next_position(self.direction))
                elif status_code == 1:
                    self.update_position()
                    self.board[self.position] = 1
                elif status_code == 2:
                    self.update_position()
                    self.found_oxygen()
                else:
                    raise ValueError(f"Unexpected game instruction: {output}")

            except StopIteration:
                print("stop")
                self.render(i)
                return None

    def shortest_route(self):
        pass

    # BFS


def next_coord(coord, cmd):
    if cmd == 1:
        return tuple(a + b for a, b in zip(coord, (0,-1)))
    if cmd == 2:
        return tuple(a + b for a, b in zip(coord, (0,1)))
    if cmd == 3:
        return tuple(a + b for a, b in zip(coord, (-1,0)))
    if cmd == 4:
        return tuple(a + b for a, b in zip(coord, (1,0)))


def maze_tester(input):
    maze_str = [
        "########",
        "#     O#",
        "### ####",
        "  # #   ",
        "  #X#   ",
        "  ###   ",
    ]
    walls = {
        (x, y)
        for y, line in enumerate(maze_str)
        for x, tile in enumerate(line) if tile == "#"
    }
    # walls = set([(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (0,1), (7,1), (0,2), (1,2), (2,2), (4,2), (5,2), (6,2), (7,2),(2,3), (4,3), (2,4), (4,4),(2,5), (4,5), (4,6), (5,6), (6,6)])
    curr_pos = (3,5)
    goal = (6,1)
    while True:
        cmd = next(input)
        next_pos = next_coord(curr_pos, cmd)
        print('next',next_pos)
        if next_pos in walls:
            yield 0
        elif next_pos == goal:
            yield 2
            curr_pos = next_pos
        else:
            yield 1
            curr_pos = next_pos


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
