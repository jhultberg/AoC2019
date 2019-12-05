def calc(data, noun = None, verb = None):
    data = list(data)
    if noun is not None:
        data[1] = noun
    if verb is not None:
        data[2] = verb
    position = 0
    while data[position] != 99:
        first = data[data[position + 1]]
        second = data[data[position + 2]]
        new = data[position + 3]
        if data[position] == 1:
            data[new] = first + second
        elif data[position] == 2:
            data[new] = first * second
        else:
            raise ValueError("Unexpected OP-code")
        position += 4

    return data


def find_noun_and_verb(data):
    for noun in range (100):
        for verb in range (100):
            result = calc(data, noun, verb)
            if result[0] == 19690720:
                return 100 *noun + verb


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    data = []
    for instruction in input:
        data.append(int(instruction))


    a = calc(data, 12, 2)
    b = find_noun_and_verb(data)
    return (a[0], b)


assert calc([1,0,0,0,99]) == [2,0,0,0,99]
assert calc([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]

