import re, math

def calc_tree(input):
     tree = {}
     for objects in input:
         tree[objects[0]] = objects[1]
     return tree

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


def translate_to_ore(tree, reaction, times = 1, div = 1, ore = []):
    print('re',reaction)
    next_level = tree[reaction[1]]
    print('nl', next_level)
    next_instructions = next_level[1]
    if len(next_instructions) == 1 and next_instructions[0][1] == 'ORE':
        print((times/div, reaction[1]))
        return (times/div, reaction[1])

    for instruction in next_instructions:
        print('in', instruction)
        print('div', div, next_level[0])
        print('mul', times, instruction[0])
        print(next_level[0], reaction[0], instruction[0])
        if next_level[0] > reaction[0]:
            ore.append(translate_to_ore(tree, instruction, instruction[0]*next_level[0], div, []))
        else:
            ore.append(translate_to_ore(tree, instruction, instruction[0]*times, div*next_level[0], []))
    return ore


def remove_nestings(l, output = []): 
    for i in l: 
        if type(i) == list: 
            remove_nestings(i, output) 
        elif type(i) == tuple and type(i[0]) == tuple and type(i[1]) == tuple:
            remove_nestings(i, output) 
        else: 
            output.append(i)
    return output

def num_ore(tree):
    print(tree)
    start = (1, 'FUEL')
    ore = remove_nestings(translate_to_ore(tree, start))
    print(ore)
    d = {}
    for pair in ore:
        if pair[1] in d:
            d[pair[1]] += pair[0]
        else:
            d[pair[1]] = pair[0]
    print(d)
    tot_ore = 0
    rest = 0
    for k, v in d.items():
        in_ore = tree[k]
        v = v - rest
        mul = math.ceil(v / in_ore[0])
        rest = mul * in_ore[0] - v 
        tot_ore += mul * in_ore[1][0][0]

    return tot_ore


def solve(path):
    with open(path) as f:
        input = list(line.strip().split(" => ") for line in f)

    reactions = list(get_reactions(input))
    print(reactions)
    tree = calc_tree(reactions)
    ore = num_ore(tree)

    return (ore, None)
