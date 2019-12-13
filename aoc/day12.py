import re, math
from itertools import permutations
from copy import deepcopy


class Moon:
    def __init__(self, x, y, z, x_vel=0, y_vel=0, z_vel=0):
        self.x = x
        self.y = y
        self.z = z
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.z_vel = z_vel

    def __repr__(self):
        return f"x={self.x}, y={self.y}, z={self.z}, x_vel={self.x_vel}, y_vel={self.y_vel}, z_vel={self.z_vel}"

    def update_position(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.z += self.z_vel


def update_velocities(moon_1, moon_2):
    for dir in ["x", "y", "z"]:
        update_velocity(moon_1, moon_2, dir)


def update_velocity(moon_1, moon_2, direction):
    if direction == "x":
        if moon_1.x > moon_2.x:
            moon_1.x_vel -= 1
            moon_2.x_vel += 1
        elif moon_1.x < moon_2.x:
            moon_1.x_vel += 1
            moon_2.x_vel -= 1
    elif direction == "y":
        if moon_1.y > moon_2.y:
            moon_1.y_vel -= 1
            moon_2.y_vel += 1
        elif moon_1.y < moon_2.y:
            moon_1.y_vel += 1
            moon_2.y_vel -= 1
    elif direction == "z":
        if moon_1.z > moon_2.z:
            moon_1.z_vel -= 1
            moon_2.z_vel += 1
        elif moon_1.z < moon_2.z:
            moon_1.z_vel += 1
            moon_2.z_vel -= 1
    else:
        raise ValueError(f"Unexpected direction for update velocity: {direction}")


def find_moons(input):
    for moon in input:
        x, y, z = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", moon).groups()
        yield Moon(int(x), int(y), int(z))


def kin_energy(moon):
    return abs(moon.x_vel) + abs(moon.y_vel) + abs(moon.z_vel)


def pot_energy(moon):
    return abs(moon.x) + abs(moon.y) + abs(moon.z)


def total_energy(moons):
    for moon in moons:
        yield pot_energy(moon) * kin_energy(moon)


def simulate(moons, steps=1, direction=None):
    moons = list(moons)
    for _ in range(steps):
        other_moons = list(moons)
        for moon in moons:
            other_moons.remove(moon)
            for other in other_moons:
                if direction is None:
                    update_velocities(moon, other)
                else:
                    update_velocity(moon, other, direction)
        for moon in moons:
            moon.update_position()
    return moons


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def split_dimension(moons, direction):  # [(p1x, v1x), (p2x, v2x), ..., [
    for moon in moons:
        if direction == "x":
            yield (moon.x, moon.x_vel)
        elif direction == "y":
            yield (moon.y, moon.y_vel)
        elif direction == "z":
            yield (moon.z, moon.z_vel)
        else:
            raise ValueError(f"Unexpected direction for split dimenson : {direction}")


def cycles_to_repetition(moons, direction):
    initial_positions = list(split_dimension(moons, direction))

    iterations = 1
    while True:
        moons = simulate(moons, direction=direction)
        if list(split_dimension(moons, direction)) == initial_positions:
            return iterations

        iterations += 1


def total_iterations_to_repetition(moons):
    cycle_x = cycles_to_repetition(deepcopy(moons), "x")
    cycle_y = cycles_to_repetition(deepcopy(moons), "y")
    cycle_z = cycles_to_repetition(deepcopy(moons), "z")

    return lcm(cycle_x, lcm(cycle_y, cycle_z))


def solve(path):
    with open(path) as f:
        input = f.readlines()

    moons = list(find_moons(input))

    energy = sum(total_energy(simulate(deepcopy(moons), 1000)))

    cycles = total_iterations_to_repetition(deepcopy(moons))

    return (energy, cycles)
