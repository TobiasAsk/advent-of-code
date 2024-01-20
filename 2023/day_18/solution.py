import sys
import re

CODE_PATTERN = re.compile(r'\(#([a-z0-9]*)\)')

DIRECTIONS = {
    'R': (1, 0),
    'D': (0, 1),
    'L': (-1, 0),
    'U': (0, -1)
}


def get_lagoon_area(trench: list[tuple[int]]):
    area = 0

    for i in range(-1, len(trench)-1):
        x, y = trench[i]
        other_x, other_y = trench[i+1]
        area += x * other_y - y * other_x
    return abs(area // 2)


def main():
    filename = sys.argv[1]
    position = (0, 0)
    trench = [position]
    lagoon_area = 0

    with open(filename) as dig_plan_file:
        for line in dig_plan_file:
            instruction_code = CODE_PATTERN.search(line.strip()).group(1)
            num_meters = int(f'0x{instruction_code[:-1]}', 16)
            lagoon_area += num_meters / 2
            direction = 'RDLU'[int(instruction_code[-1])]
            x, y = position
            dx, dy = DIRECTIONS[direction]
            position = (x+dx*num_meters, y+dy*num_meters)
            trench.append(position)

    lagoon_area += get_lagoon_area(trench[:-1]) + 1
    print(int(lagoon_area))


if __name__ == '__main__':
    main()
