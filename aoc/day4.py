def is_valid_password(i):
    string = str(i)
    latest = 1
    two_of_same = False
    invalid = False
    for j in string:
        if int(j) < int(latest):
            invalid = True
        elif j == latest:
            two_of_same = True
        latest = j
    if invalid:
        return False
    elif two_of_same:
        return True
    else:
        return False


def has_even_number_adjacent(i):
    string = str(i)
    adjacent = 1
    latest = string[0]
    groups = []
    for j in string[1:]:
        if j == latest:
            adjacent += 1
        else:
            groups.append(adjacent)
            adjacent = 1
        latest = j

    groups.append(adjacent)
    return 2 in groups


def is_valid_password_2(i):
    if not is_valid_password(i):
        return False
    return has_even_number_adjacent(i)


def solve(start, stop):
    passwords1 = 0
    passwords2 = 0
    for i in range(start, stop + 1):
        if is_valid_password(i):
            passwords1 += 1
        if is_valid_password_2(i):
            passwords2 += 1
    return (passwords1, passwords2)
