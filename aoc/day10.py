import math


def print_asteroids(asteroids):
    x_size = max(asteroids)[0] + 1
    y_size = max(asteroids)[1] + 1

    for y in range(y_size):
        for x in range(x_size):
            if (x, y) in asteroids:
                print('#', end="")
            else:
                print('.', end="")
        print()


def is_colinear(asteroid, curr_asteroid, prev_asteroid):
    return prev_asteroid[0] * (curr_asteroid[1] - asteroid[1]) + curr_asteroid[0] * (asteroid[1] - prev_asteroid[1]) + asteroid[0] * (prev_asteroid[1] - curr_asteroid[1]) == 0


def is_between_points(asteroid, curr_asteroid, prev_asteroid):
    if not is_colinear(prev_asteroid, curr_asteroid, asteroid):
        return False
    return abs(math.dist(curr_asteroid, asteroid) + math.dist(asteroid, prev_asteroid) - math.dist(curr_asteroid, prev_asteroid)) < 0.5

def find_asteroids(stars, curr_asteroid):
    seen_asteroids = set()
    for asteroid in stars:
        if asteroid == curr_asteroid:
            continue
        blocked = False
        for seen in seen_asteroids:
            if not is_colinear(seen, asteroid, curr_asteroid):
                # Asteroids not on the same line, cannot block eachother
                continue
            elif is_between_points(asteroid, curr_asteroid, seen):
                # The new asteroid blocks one we have saved
                seen_asteroids.remove(seen)
            else:
                # The asteroid is blocked by one prevoisly checked
                blocked = True
            break

        if not blocked:
            seen_asteroids.add(asteroid)
    return seen_asteroids


def find_most_asteroids(stars):
    best_coordinate = (-1,-1)
    most_asteroids = 0
    for coord in stars:
        seen_asteroids = len(find_asteroids(stars, coord))
        print(coord, seen_asteroids)
        if seen_asteroids > most_asteroids:
            most_asteroids = seen_asteroids
            best_coordinate = coord
    #print_asteroids(find_asteroids(stars, (5,8)))
    return (best_coordinate, most_asteroids)


def vaporize(stars, asteroid):
    stars.remove(asteroid)


def find_angle_from_vertical(station, asteroid):
    # Call atan2(x, y) instead of atan2(y, x) since want angle from y-axis, not x-axis
    angle = math.atan2((asteroid[0] - station[0]), (asteroid[1] - station[1])) * 180 / math.pi
    if angle < 0:
        return 360 + angle
    return angle


def destroy_asteroids(stars, station, target):
    seen_asteroids = find_asteroids(stars, station)
    angles = {}
    for asteroid in seen_asteroids:
        angles[asteroid] = find_angle_from_vertical(station, asteroid)
    # This happens to work for py3.8....
    angles = {k: v for k, v in sorted(angles.items(), key=lambda item: item[1])}

    target_sum = 0
    for i, asteroid in enumerate(angles):
        if i < target:
            vaporize(stars, asteroid)
            target_sum = 100 * asteroid[0] + asteroid[1]

    return target_sum


def find_stars(input):
    stars = set()
    for y, line in enumerate(input):
        for x, val in enumerate(line):
            if val == '#':
                stars.add((x, y))

    return stars

def solve(path):
    with open(path) as f:
        input = f.readlines()

    stars = find_stars(input)

    a = find_most_asteroids(stars)
    b = destroy_asteroids(stars, a[0], 200)
    return (a[1], b)
