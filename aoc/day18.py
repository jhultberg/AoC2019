import re
from collections import deque
from itertools import count


class Maze:
    def __init__(self, walls, doors, name_to_doors, keys, position):
        self.walls = walls
        self.doors = doors
        self.name_to_doors = name_to_doors
        self.keys = keys
        self.start = position
        self.position = position

    def __repr__(self):
        return f"walls = {self.walls} \n  doors = {self.doors} \n  keys = {self.keys} \n position = {self.position}"

    def __eq__(self, rhs):
        return (
            self.walls == rhs.walls
            and self.doors == rhs.doors
            and self.keys == rhs.keys
            and self.position == rhs.position
        )

    def find_neighbors(self, visited):
        neighbors = deque()
        neighbor = (self.position[0] + 1, self.position[1])
        if neighbor not in self.walls and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (self.position[0] - 1, self.position[1])
        if neighbor not in self.walls and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (self.position[0], self.position[1] + 1)
        if neighbor not in self.walls and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (self.position[0], self.position[1] - 1)
        if neighbor not in self.walls and neighbor not in visited:
            neighbors.append(neighbor)

        return neighbors


    def bfs(self, start):
        nodes = deque([([start],set())])
        visited = set()

        while nodes:
            path, blockers = nodes.popleft()
            print(path)
            node = path[-1]
            if node in self.keys and node != start:
                 yield(self.keys[node], len(path), blockers)
            if node in self.doors:
                blockers.add(self.doors[node])

            visited.add(node)
            self.position = node
            neighbors = self.find_neighbors(visited)
            for n in neighbors:
                nodes += ([path + [n]], blockers)


    def collect_all_keys(self):
        all_distances = []
        for key in self.keys:
            all_distances.append((self.keys[key], list(self.bfs(key))))
        print(all_distances)








def parse_input(input_data):
    walls = set()
    doors = {}
    name_to_doors = {}
    keys = {}
    position = None

    for y, line in enumerate(input_data):
        for x, tile in enumerate(line):
            if tile == "#":
                walls.add((x,y))
            elif re.match(r"[A-Z]", tile):
                doors[(x,y)] = tile
                name_to_doors[tile] = (x,y)
            elif re.match(r"[a-z]", tile):
                keys[(x,y)] = tile
            elif tile == "@":
                position = (x,y)
            else:
                continue
    return Maze(walls, doors, name_to_doors, keys, position)


def solve(path):
    with open(path) as f:
        input_data = f.readlines()
    data = [line.rstrip() for line in input_data]

    maze = parse_input(data)

    steps = maze.collect_all_keys()

    return (steps, None)
