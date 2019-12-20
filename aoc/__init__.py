import sys

from . import (
    day1,
    day2,
    day3,
    day4,
    day5,
    day6,
    day7,
    day8,
    day9,
    day10,
    day11,
    day12,
    day13,
    day14,
    day15,
    day16,
    day17,
    day18,
    day19,
    day20,
)


def main():
    if len(sys.argv) < 2:
        print("Usage: aoc <day> [args...]")
        exit(0)

    day = int(sys.argv[1])
    if day == 1:
        a, b = day1.solve(sys.argv[2])
    elif day == 2:
        a, b = day2.solve(sys.argv[2])
    elif day == 3:
        a, b = day3.solve(sys.argv[2])
    elif day == 4:
        a, b = day4.solve(int(sys.argv[2]), int(sys.argv[3]))
    elif day == 5:
        a, b = day5.solve(sys.argv[2])
    elif day == 6:
        a, b = day6.solve(sys.argv[2])
    elif day == 7:
        a, b = day7.solve(sys.argv[2])
    elif day == 8:
        a, b = day8.solve(sys.argv[2])
    elif day == 9:
        a, b = day9.solve(sys.argv[2])
    elif day == 10:
        a, b = day10.solve(sys.argv[2])
    elif day == 11:
        a, b = day11.solve(sys.argv[2])
    elif day == 12:
        a, b = day12.solve(sys.argv[2])
    elif day == 13:
        a, b = day13.solve(sys.argv[2])
    elif day == 14:
        a, b = day14.solve(sys.argv[2])
    elif day == 15:
        a, b = day15.solve(sys.argv[2])
    elif day == 16:
        a, b = day16.solve(sys.argv[2])
    elif day == 17:
        a, b = day17.solve(sys.argv[2])
    elif day == 18:
        a, b = day18.solve(sys.argv[2])
    elif day == 19:
        a, b = day19.solve(sys.argv[2])
    elif day == 20:
        a, b = day20.solve(sys.argv[2])
    else:
        print("No solution for the given day ({})".format(day))
        exit(1)

    print("A:", a)
    if b is not None:
        print("B:", b)
