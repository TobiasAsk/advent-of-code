import sys
import re
import operator
from functools import reduce


RED_CUBES_PATTERN = re.compile(r'(\d+) red')
GREEN_CUBES_PATTERN = re.compile(r'(\d+) green')
BLUE_CUBES_PATTERN = re.compile(r'(\d+) blue')
PATTERNS = [
    RED_CUBES_PATTERN,
    GREEN_CUBES_PATTERN,
    BLUE_CUBES_PATTERN
]


def max_num_cubes(pattern, line):
    all_nums = [int(n) for n in pattern.findall(line)]
    return max(all_nums)


def main():
    filename = sys.argv[1]
    power_sum = 0

    with open(filename) as game_info_file:
        for line in game_info_file:
            min_required_cubes = [max_num_cubes(p, line) for p in PATTERNS]
            power_sum += reduce(operator.mul, min_required_cubes)

    print(f'Sum is {power_sum}')


if __name__ == '__main__':
    main()
