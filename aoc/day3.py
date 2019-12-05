def distance(x, y):
    return abs(x) + abs(y)


def calc_coords(instructions):
    coords = set()
    coord = (0, 0)
    for step in instructions:
        if step[0] == "R":
            for i in range(1, int(step[1:]) + 1):
                new_coord = (coord[0] + i, coord[1])
                coords.add(new_coord)
        elif step[0] == "L":
            for i in range(1, int(step[1:]) + 1):
                new_coord = (coord[0] - i, coord[1])
                coords.add(new_coord)
        elif step[0] == "U":
            for i in range(1, int(step[1:]) + 1):
                new_coord = (coord[0], coord[1] + i)
                coords.add(new_coord)
        elif step[0] == "D":
            for i in range(1, int(step[1:]) + 1):
                new_coord = (coord[0], coord[1] - i)
                coords.add(new_coord)
        coord = new_coord
    return coords


def calc_intersections(visited_coords):
    string1 = visited_coords[0]
    string2 = visited_coords[1]

    intersections = string1.intersection(string2)
    return intersections


def find_closest_intersection(intersections):
    closest = float("inf")
    for intersection in intersections:
        dist = distance(intersection[0], intersection[1])
        if dist < closest:
            closest = dist
    return closest


def closest_distance(instructions):
    visited_coords = []
    for instruction in instructions:
        visited_coords.append(calc_coords(instruction))

    intersections = calc_intersections(visited_coords)

    return find_closest_intersection(intersections)


def intersections_with_steps(coords):
    string1 = coords[0][0]
    string2 = coords[1][0]

    coord_to_step1 = coords[0][1]
    coord_to_step2 = coords[1][1]

    intersections = string1.intersection(string2)

    closest = float("inf")
    for intersection in intersections:
        dist = coord_to_step1[intersection] + coord_to_step2[intersection]
        if dist < closest:
            closest = dist
    return closest


def calc_coords_with_steps(instructions):
    coords = set()
    coord_to_step = {}
    coord = (0, 0)
    steps = 0
    for step in instructions:
        if step[0] == "R":
            for i in range(1, int(step[1:]) + 1):
                steps += 1
                new_coord = (coord[0] + i, coord[1])
                coord_to_step[new_coord] = steps
                coords.add(new_coord)
        elif step[0] == "L":
            for i in range(1, int(step[1:]) + 1):
                steps += 1
                new_coord = (coord[0] - i, coord[1])
                coord_to_step[new_coord] = steps
                coords.add(new_coord)
        elif step[0] == "U":
            for i in range(1, int(step[1:]) + 1):
                steps += 1
                new_coord = (coord[0], coord[1] + i)
                coord_to_step[new_coord] = steps
                coords.add(new_coord)
        elif step[0] == "D":
            for i in range(1, int(step[1:]) + 1):
                steps += 1
                new_coord = (coord[0], coord[1] - i)
                coord_to_step[new_coord] = steps
                coords.add(new_coord)
        coord = new_coord
    return (coords, coord_to_step)


def shortest_distance(instructions):
    visited_coords = []
    for instruction in instructions:
        visited_coords.append(calc_coords_with_steps(instruction))

    return intersections_with_steps(visited_coords)


def solve(path):
    input_data = []
    with open(path) as f:
        for line in f:
            input_data.append(line.strip().split(","))

    a = closest_distance(input_data)
    b = shortest_distance(input_data)

    return (a, b)
