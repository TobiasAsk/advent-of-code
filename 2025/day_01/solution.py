'''Modulo refresher.'''

import sys
import re

ROTATION_PATTERN = re.compile(r'([LR])(\d+)')


def main():
    filename = sys.argv[1]
    with open(filename) as rotations_file:
        rotations = rotations_file.read().splitlines()

    current_num = 50
    zero_count = 0
    for rotation in rotations:
        match = ROTATION_PATTERN.search(rotation)
        direction, num_steps = match.group(1), int(match.group(2))
        sign = 1 if direction == 'R' else -1
        new_num_mod_only = current_num + sign*(num_steps % 100)
        zero_count += num_steps // 100
        zero_count += current_num > 0 and (new_num_mod_only < 0 or new_num_mod_only > 100)
        current_num = (current_num + sign*num_steps) % 100
        zero_count += current_num == 0
    print(zero_count)


if __name__ == '__main__':
    main()
