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
        # input()

    def movements(self):
        while True:
            yield self.direction

    def move(self, cmd):
        self.direction = cmd
        status = next(self.droid)
        return status

    def find_next_direction(self):
        for i in range(1, 5):
            if self.find_next_position(i) not in self.visited:
                return i

    def explore(self):
        for i in count():
            try:
                cmd = self.find_next_direction()
                if cmd is None:
                    if not self.route:
                        self.render(i)
                        return (self.shortest_route(), self.fill_with_oxygen())
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
                self.render(i)
                return None

    def find_neighbors(self, visited):
        neighbors = deque()
        neighbor = (self.position[0] + 1, self.position[1])
        if self.board[neighbor] != 0 and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (self.position[0] - 1, self.position[1])
        if self.board[neighbor] != 0 and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (self.position[0], self.position[1] + 1)
        if self.board[neighbor] != 0 and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (self.position[0], self.position[1] - 1)
        if self.board[neighbor] != 0 and neighbor not in visited:
            neighbors.append(neighbor)

        return neighbors

    def find_distance(self, relations, fr, to):
        pos = fr
        for i in count():
            pos = relations[pos]
            if pos == to:
                return i + 1

    def shortest_route(self):
        visited = set()
        nodes = deque([self.position])
        relations = {}

        while nodes:
            node = nodes.popleft()
            if node == self.oxygen:
                return self.find_distance(relations, self.oxygen, (0, 0))
            visited.add(node)
            self.position = node
            neighbors = self.find_neighbors(visited)

            for n in neighbors:
                relations[n] = self.position
            nodes += neighbors

    def fill_with_oxygen(self):
        visited = set()
        self.position = self.oxygen
        nodes = deque([self.position])
        relations = {}

        while nodes:
            node = nodes.popleft()
            self.board[(node)] = 2
            visited.add(node)
            self.position = node
            neighbors = self.find_neighbors(visited)

            for n in neighbors:
                relations[n] = self.position
            nodes += neighbors
        return self.find_distance(relations, self.position, self.oxygen)


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    program = []
    for instruction in input:
        program.append(int(instruction))

    a, b = Droid(program).explore()

    return (a, b)
