from .intcode import run
from collections import defaultdict
from itertools import count
from operator import itemgetter


class Droid:

    DIR_NORTH = 1
    DIR_SOUTH = 2
    DIR_WEST = 3
    DIR_EAST = 4

    def __init__(self, program):
        self.program = program
        self.board = defaultdict()
        self.position = (0, 0)
        self.oxygen = (None, None)
        self.direction = self.DIR_NORTH

        self.board[(0,0)] = 1


    def render(self):
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
        self.position = self.find_next_position()

    def find_next_position(self):
        if self.direction == self.DIR_NORTH:
            return (self.position[0], self.position[1] + 1)
        elif self.direction == self.DIR_SOUTH:
            return (self.position[0], self.position[1] - 1)
        elif self.direction == self.DIR_EAST:
            return (self.position[0] + 1, self.position[1])
        elif self.direction == self.DIR_WEST:
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


    def movements(self):
        while True:
            #print('mov', self.direction)
            yield self.direction


    def explore(self):
        droid = run(self.program, self.movements())
        for i in count():
            try:
                status_code = next(droid)
                #print(status_code)
                if status_code == 0:
                    #wall
                    # turn and try again
                    self.board[self.find_next_position()] = 0
                    self.turn_left()
                elif status_code == 1:
                    #moved
                    #update position
                    self.update_position()
                    # if already mapped should probably turn here aswell?
                   # if self.board[self.position] == 1:
                        #already been here, try another route
                    #    self.turn_left()
                    #else:
                    self.board[self.position] = 1
                elif status_code == 2:
                    #found oxygen
                    self.update_position()
                    self.found_oxygen()
                    print(self.oxygen)
                    #return self.shortest_route()
                else:
                    raise ValueError(f"Unexpected game instruction: {output}")
                print(self.position)
                self.render()
            except StopIteration:
                print('stop')
                #self.render()
                return (0, None)


    def shortest_route(self): pass
        #BFS



def find_oxygen(program):
    a, b = Droid(program).explore()
    return (a, b)



def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    input_data = []
    for instruction in input:
        input_data.append(int(instruction))

    a = find_oxygen(input_data)[0]

    return (a, None)
