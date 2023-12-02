import sys
import re


RED_CUBES_PATTERN = re.compile(r'(\d+) red')
GREEN_CUBES_PATTERN = re.compile(r'(\d+) green')
BLUE_CUBES_PATTERN = re.compile(r'(\d+) blue')
PATTERNS = [
    RED_CUBES_PATTERN,
    GREEN_CUBES_PATTERN,
    BLUE_CUBES_PATTERN
]
MAX = (12, 13, 14)  # r, g, b


def max_num_cubes(pattern, line):
    all_nums = [int(n) for n in pattern.findall(line)]
    return max(all_nums)


def main():
    filename = sys.argv[1]
    possible_ids_sum = 0

    with open(filename) as game_info_file:
        for line_num, line in enumerate(game_info_file):
            max_nums = [max_num_cubes(p, line) for p in PATTERNS]
            if all(max_nums[i] <= MAX[i] for i in range(3)):
                possible_ids_sum += (line_num+1)

    print(f'Sum is {possible_ids_sum}')


if __name__ == '__main__':
    main()
