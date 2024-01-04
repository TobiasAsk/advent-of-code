import sys

TILT_DIRECTIONS = [
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, 0)
]


def parse_rock_map(map_lines: list[str]) -> tuple[set[tuple[int]]]:
    height = len(map_lines)
    width = len(map_lines[0])
    rolling_rocks = [(x, y) for y in range(height) for x in range(width) if
                     map_lines[y][x] == 'O']
    static_rocks = [(x, y) for y in range(height) for x in range(width) if
                    map_lines[y][x] == '#']
    return rolling_rocks, static_rocks, (height, width)


def print_rocks(rolling_rocks, static_rocks, dimensions):
    height, width = dimensions
    for y in range(height):
        print(''.join('O' if (x, y) in rolling_rocks else
                      '#' if (x, y) in static_rocks else
                      '.' for x in range(width)))
    print()


def calculate_load(rolling_rocks, platform_height):
    return sum(platform_height - y for _, y in rolling_rocks)


def tilt(rolling_rocks, static_rocks, direction, platform_dimensions):
    height, width = platform_dimensions
    dx, dy = direction
    moving = True

    while moving:
        moving = False
        for i in range(len(rolling_rocks)):
            rock_x, rock_y = rolling_rocks[i]
            new_rock_x, new_rock_y = rock_x + dx, rock_y + dy
            if (0 <= new_rock_x < width and 0 <= new_rock_y < height and
                    (new_rock_x, new_rock_y) not in rolling_rocks + static_rocks):
                rolling_rocks[i] = (new_rock_x, new_rock_y)
                moving = True


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        rolling_rocks, static_rocks, dimensions = parse_rock_map(map_file.read().splitlines())

    target_num_cycles = 1000000000
    rock_hashes = []
    cycles = 0
    skipped = False

    while cycles < target_num_cycles:
        for direction in TILT_DIRECTIONS:
            tilt(rolling_rocks, static_rocks, direction, dimensions)

        cycles += 1
        rock_hash = hash(tuple(sorted(rolling_rocks)))

        if (not skipped and rock_hash in rock_hashes):
            cycle_length = cycles - rock_hashes.index(rock_hash) - 1
            num_skipped_cycles = (target_num_cycles - cycles) // cycle_length
            cycles += num_skipped_cycles * cycle_length
            skipped = True

        rock_hashes.append(rock_hash)

    load = calculate_load(rolling_rocks, dimensions[0])
    print(load)


if __name__ == '__main__':
    main()
