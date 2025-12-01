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
        current_num = (current_num + num_steps) % 100 if direction == 'R' else (current_num - num_steps) % 100
        if current_num == 0:
            zero_count += 1
    print(zero_count)

if __name__ == '__main__':
    main()
