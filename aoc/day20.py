import re
from collections import defaultdict, deque


class Maze:
    def __init__(self, walls, portals, tunnels):
        self.walls = walls
        self.start = portals[0]
        self.end = portals[1]
        self.outer_to_inner = portals[2]
        self.inner_to_outer = portals[3]
        self.inner_portals = portals[4]
        self.outer_portals = portals[5]
        self.tunnels = tunnels
        self.tunnels.remove(self.start)
        self.tunnels.remove(self.end)

    def find_neighbors(self, node, visited):
        neighbors = deque()
        neighbor = (node[0] + 1, node[1])
        if (
            neighbor in self.tunnels or neighbor == self.end
        ) and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (node[0] - 1, node[1])
        if (
            neighbor in self.tunnels or neighbor == self.end
        ) and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (node[0], node[1] + 1)
        if (
            neighbor in self.tunnels or neighbor == self.end
        ) and neighbor not in visited:
            neighbors.append(neighbor)
        neighbor = (node[0], node[1] - 1)
        if (
            neighbor in self.tunnels or neighbor == self.end
        ) and neighbor not in visited:
            neighbors.append(neighbor)

        return neighbors

    def shortest_distance(self, check_layers=False):
        nodes = deque([(self.start, 0, 0)])
        visited = defaultdict(set)

        while nodes:
            node, layer, distance = nodes.popleft()
            if node == self.end and layer == 0:
                return distance
            distance += 1
            visited[layer].add(node)

            if node in self.inner_to_outer:
                if check_layers:
                    layer += 1
                distance += 1
                node = self.inner_to_outer[node]
                visited[layer].add(node)
            elif node in self.outer_to_inner and layer != 0:
                if check_layers:
                    layer -= 1
                distance += 1
                node = self.outer_to_inner[node]
                visited[layer].add(node)

            neighbors = self.find_neighbors(node, visited[layer])

            for n in neighbors:
                if n == self.end and layer != 0:
                    continue
                nodes.append((n, layer, distance))


def find_portals(input_data, tunnels):
    inner_portals = {}
    outer_portals = {}
    x_size = len(input_data[0])
    y_size = len(input_data)

    for y, line in enumerate(input_data):
        for x, tile in enumerate(line):
            if re.match(r"[A-Z]", tile):
                if re.match(r"[A-Z]", input_data[y][x + 1]):
                    if (x + 2, y) in tunnels and x + 2 > x_size // 2:
                        inner_portals[(x + 2, y)] = tile + input_data[y][x + 1]
                    elif (x + 2, y) in tunnels and x + 2 < x_size // 2:
                        outer_portals[(x + 2, y)] = tile + input_data[y][x + 1]
                    elif (x - 1, y) in tunnels and x - 1 > x_size // 2:
                        outer_portals[(x - 1, y)] = tile + input_data[y][x + 1]
                    elif (x - 1, y) in tunnels and x - 1 < x_size // 2:
                        inner_portals[(x - 1, y)] = tile + input_data[y][x + 1]
                elif re.match(r"[A-Z]", input_data[y + 1][x]):
                    if (x, y + 2) in tunnels and y + 2 > y_size // 2:
                        inner_portals[(x, y + 2)] = tile + input_data[y + 1][x]
                    elif (x, y + 2) in tunnels and y + 2 < y_size // 2:
                        outer_portals[(x, y + 2)] = tile + input_data[y + 1][x]
                    elif (x, y - 1) in tunnels and y - 1 > y_size // 2:
                        outer_portals[(x, y - 1)] = tile + input_data[y + 1][x]
                    elif (x, y - 1) in tunnels and y - 1 < y_size // 2:
                        inner_portals[(x, y - 1)] = tile + input_data[y + 1][x]

    outer_to_inner = {}
    inner_to_outer = {}
    flipped_outer = {v: k for k, v in outer_portals.items()}
    for k, v in inner_portals.items():
        inner_to_outer[k] = flipped_outer[v]
        outer_to_inner[flipped_outer[v]] = k
    start = flipped_outer["AA"]
    end = flipped_outer["ZZ"]
    return (start, end, outer_to_inner, inner_to_outer, inner_portals, outer_portals)


def parse_input(input_data):
    walls = set()
    tunnels = set()

    for y, line in enumerate(input_data):
        for x, tile in enumerate(line):
            if tile == "#":
                walls.add((x, y))
            elif tile == ".":
                tunnels.add((x, y))
            else:
                continue

    portals = find_portals(input_data, tunnels)
    return Maze(walls, portals, tunnels)


def solve(path):
    with open(path) as f:
        input_data = f.readlines()
    data = [line[:-1] for line in input_data]

    maze = parse_input(data)

    a = maze.shortest_distance()
    b = maze.shortest_distance(check_layers=True)

    return (a, b)
