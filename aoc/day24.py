from operator import itemgetter
from collections import defaultdict


def state_to_string(state):
    s = ""
    max_x = max(state, key=itemgetter(0))[0] + 1
    max_y = max(state, key=itemgetter(1))[1] + 1
    for y in range(max_y):
        for x in range(max_x):
            s += str(state[(x, y)])
    return s


def biodiversity_rating(eris):
    st = state_to_string(eris)
    rating = 0
    for i, s in enumerate(st):
        rating += int(s) * (2 ** i)
    return rating


def next_state(state):
    new_state = defaultdict(int)
    max_x = max(state, key=itemgetter(0))[0] + 1
    max_y = max(state, key=itemgetter(1))[1] + 1
    for y in range(max_y):
        for x in range(max_x):
            neighbors = [
                state[(x - 1, y)],
                state[(x + 1, y)],
                state[(x, y - 1)],
                state[(x, y + 1)],
            ]
            if state[(x, y)] == 1 and sum(neighbors) != 1:
                new_state[(x, y)] = 0
            elif state[(x, y)] == 0 and (sum(neighbors) == 1 or sum(neighbors) == 2):
                new_state[(x, y)] = 1
            else:
                new_state[(x, y)] = state[(x, y)]
    return new_state


def biodiversity(eris):
    prev_states = set()

    while state_to_string(eris) not in prev_states:
        prev_states.add(state_to_string(eris))
        eris = next_state(eris)

    return biodiversity_rating(eris)


def find_neighbors(state, x, y, level):
    curr = state[level]
    above = defaultdict(int)
    if level + 1 in state:
        above = state[level + 1]
    below = defaultdict(int)
    if level - 1 in state:
        below = state[level - 1]

    if x == 0:
        if y == 0:
            return [curr[(x, y + 1)], curr[(x + 1, y)], below[(2, 1)], below[(1, 2)]]
        elif y == 4:
            return [curr[(x, y - 1)], curr[(x + 1, y)], below[(2, 3)], below[(1, 2)]]
        else:
            return [curr[(x, y + 1)], curr[(x, y - 1)], curr[(x + 1, y)], below[(1, 2)]]
    elif x == 4:
        if y == 0:
            return [curr[(x, y + 1)], curr[(x - 1, y)], below[(2, 1)], below[(3, 2)]]
        elif y == 4:
            return [curr[(x, y - 1)], curr[(x - 1, y)], below[(2, 3)], below[(3, 2)]]
        else:
            return [curr[(x, y + 1)], curr[(x, y - 1)], curr[(x - 1, y)], below[(3, 2)]]
    elif y == 0:
        return [curr[(x + 1, y)], curr[(x - 1, y)], curr[(x, y + 1)], below[(2, 1)]]
    elif y == 4:
        return [curr[(x + 1, y)], curr[(x - 1, y)], curr[(x, y - 1)], below[(2, 3)]]

    elif x == 1 and y == 2:
        return [
            curr[(x - 1, y)],
            curr[(x, y - 1)],
            curr[(x, y + 1)],
            above[(0, 0)],
            above[(0, 1)],
            above[(0, 2)],
            above[(0, 3)],
            above[(0, 4)],
        ]

    elif x == 3 and y == 2:
        return [
            curr[(x + 1, y)],
            curr[(x, y - 1)],
            curr[(x, y + 1)],
            above[(4, 0)],
            above[(4, 1)],
            above[(4, 2)],
            above[(4, 3)],
            above[(4, 4)],
        ]

    elif x == 2 and y == 1:
        return [
            curr[(x, y - 1)],
            curr[(x - 1, y)],
            curr[(x + 1, y)],
            above[(0, 0)],
            above[(1, 0)],
            above[(2, 0)],
            above[(3, 0)],
            above[(4, 0)],
        ]

    elif x == 2 and y == 3:
        return [
            curr[(x, y + 1)],
            curr[(x - 1, y)],
            curr[(x + 1, y)],
            above[(0, 4)],
            above[(1, 4)],
            above[(2, 4)],
            above[(3, 4)],
            above[(4, 4)],
        ]

    else:
        return [curr[(x - 1, y)], curr[(x + 1, y)], curr[(x, y - 1)], curr[(x, y + 1)]]


def bug_on_outer_edge(state):
    level = state[max(k for k, v in state.items())]
    return (
        level[(0, 0)] == 1
        or level[(0, 1)] == 1
        or level[(0, 2)] == 1
        or level[(0, 3)] == 1
        or level[(0, 4)] == 1
        or level[(1, 0)] == 1
        or level[(2, 0)] == 1
        or level[(3, 0)] == 1
        or level[(4, 0)] == 1
        or level[(4, 1)] == 1
        or level[(4, 2)] == 1
        or level[(4, 3)] == 1
        or level[(4, 4)] == 1
        or level[(4, 1)] == 1
        or level[(4, 2)] == 1
        or level[(4, 3)] == 1
    )


def bug_on_inner_edge(state):
    level = state[min(k for k, v in state.items())]
    return (
        level[(2, 3)] == 1
        or level[(2, 1)] == 1
        or level[(1, 2)] == 1
        or level[(3, 2)] == 1
    )


def next_recursive_state(state):
    new_state = {}

    if bug_on_outer_edge(state):
        state[max(k for k, v in state.items()) + 1] = defaultdict(int)
    if bug_on_inner_edge(state):
        state[min(k for k, v in state.items()) - 1] = defaultdict(int)

    for i, level in state.items():
        new_level = defaultdict(int)
        for y in range(5):
            for x in range(5):
                if x == 2 and y == 2:
                    # middle tile! should not be counted, only ?
                    # so setting it as 0 so it will not be counted
                    new_level[(x, y)] = 0
                    continue
                neighbors = find_neighbors(state, x, y, i)
                if level[(x, y)] == 1 and sum(neighbors) != 1:
                    new_level[(x, y)] = 0
                elif level[(x, y)] == 0 and (
                    sum(neighbors) == 1 or sum(neighbors) == 2
                ):
                    new_level[(x, y)] = 1
                else:
                    new_level[(x, y)] = level[(x, y)]
        new_state[i] = new_level
    return new_state


def count_bugs(state):
    bugs = 0
    for _, level in state.items():
        bugs += sum(value == 1 for value in level.values())
    return bugs


def recursive_biodiversity(initial, iterations):
    state = {0: initial}
    for i in range(iterations):
        state = next_recursive_state(state)
    return count_bugs(state)


def parse_input(input):
    eris = defaultdict(int)
    for y, line in enumerate(input):
        for x, tile in enumerate(line):
            if tile == "#":
                eris[(x, y)] = 1
            elif tile == ".":
                eris[(x, y)] = 0
            else:
                raise ValueError(f"unexpected tile from input {tile}")
    return eris


def solve(path):
    with open(path) as f:
        input_data = f.readlines()
    input_data = [line[:-1] for line in input_data]

    eris = parse_input(input_data)

    a = biodiversity(eris)
    b = recursive_biodiversity(eris, 200)

    return (a, b)
