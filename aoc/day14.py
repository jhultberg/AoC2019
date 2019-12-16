import re, math
from collections import defaultdict
from itertools import count


def get_reactions(input):
    for instruction in input:
        key = instruction[1]
        values = instruction[0].strip().split(", ")
        key_pair = re.match(r"(\d+) ([A-Z]+)", key).groups()
        value_pairs = []
        for value in values:
            split_vals = re.match(r"(\d+) ([A-Z]+)", value).groups()
            value_pairs.append((int(split_vals[0]), split_vals[1]))
        yield (key_pair[1], (int(key_pair[0]), value_pairs))


class Reactor:
    def __init__(self, tree):
        self.tree = tree
        self.total_ore = 0
        self.leftovers = defaultdict(int)

    def calc_cost(self, to_produce, num):
        if to_produce == "ORE":
            self.total_ore += num
            return

        if self.leftovers[to_produce] != 0:
            num -= self.leftovers[to_produce]
        if num < 0:
            self.leftovers[to_produce] = abs(num)
            return
        else:
            self.leftovers[to_produce] = 0

        min_quantity, ingredients = self.tree[to_produce]
        batches = (num + min_quantity - 1) // min_quantity
        self.leftovers[to_produce] += batches * min_quantity - num
        for num_req_per_batch, ingredient_name in ingredients:
            self.calc_cost(ingredient_name, num_req_per_batch * batches)


def translate_to_ore(tree, num_wanted=1):
    reactor = Reactor(tree)
    reactor.calc_cost("FUEL", num_wanted)
    return reactor.total_ore


def find_max_fuel(tree, delta, start):
    for i in count(start, delta):
        if translate_to_ore(tree, i) > 1_000_000_000_000:
            if delta == 1:
                return i - 1
            return find_max_fuel(tree, delta // 10, i - delta)


def solve(path):
    with open(path) as f:
        input = list(line.strip().split(" => ") for line in f)

    reactions = list(get_reactions(input))
    tree = dict(reactions)
    ore = translate_to_ore(tree)
    max_fuel = find_max_fuel(tree, 1_000_000, 1)

    return (ore, max_fuel)
