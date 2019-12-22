import re


def shuffle(program, deck):
    for instruction in program:
        if instruction[0] == "cut":
            val = instruction[1]
            deck = deck[val:] + deck[:val]
        elif instruction[0] == "incr":
            val = instruction[1]
            new_deck = [0] * len(deck)
            for pos, card in enumerate(deck):
                new_deck[pos * val % len(deck)] = card
            deck = new_deck
        elif instruction[0] == "stack":
            deck.reverse()
        else:
            raise ValueError(f"Unexpected instruction in shuffle: {instruction[0]}")
    return deck


def mega_shuffle(program, deck_size, shuffle_times):
    # Python cannot overflow integers! Will raise memoryError instead
    deck = list(range(deck_size))
    for _ in range(shuffle_times):
        print(deck.index(0))
        deck = shuffle(program, deck)
    return deck


def parse_input(input):
    parsed_program = []
    for row in input:
        if re.match(r"([a-z\s]*) (-?\d*)\n", row):
            inst, number = re.match(r"([a-z\s]*) (-?\d*)\n", row).groups()
        else:
            inst = re.match(r"([a-z\s]*)\n", row)
            inst = inst.group(0)
        if inst == "cut":
            parsed_program.append(("cut", int(number)))
        elif inst == "deal with increment":
            parsed_program.append(("incr", int(number)))
        elif inst == "deal into new stack\n":
            parsed_program.append(("stack", None))
        else:
            raise ValueError(f"Unexpected instruction to parse: {inst}")
    return parsed_program


def solve(path):
    with open(path) as f:
        input = f.readlines()

    program = parse_input(input)

    shuffeled = shuffle(program, list(range(10007)))
    a = shuffeled.index(2019)

    mega_deck_size = 119315717514047
    no_shufflings = 101741582076661
    # mega_shuffeled = mega_shuffle(program, mega_deck_size, no_shufflings)
    # b = mega_shuffeled[2020]
    b = 0
    return (a, b)
