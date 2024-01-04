import sys

TILT_DIRECTIONS = [
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, 0)
]


def parse_rock_map(map_lines: list[str]) -> list[tuple[int]]:
    height = len(map_lines)
    width = len(map_lines[0])
    rolling_rocks = [(x, y) for y in range(height) for x in range(width) if
                     map_lines[y][x] == 'O']
    static_rocks = [(x, y) for y in range(height) for x in range(width) if
                    map_lines[y][x] == '#']
    free = [[True if map_lines[y][x] == '.' else False for x in range(width)] for y in range(height)]
    return rolling_rocks, static_rocks, free


def print_rocks(rolling_rocks, static_rocks, map_rows):
    height, width = len(map_rows), len(map_rows[0])
    for y in range(height):
        print(''.join('O' if (x, y) in rolling_rocks else
                      '#' if (x, y) in static_rocks else
                      '.' for x in range(width)))
    print()


def calculate_load(rolling_rocks, platform_height):
    return sum(platform_height - y for _, y in rolling_rocks)


def tilt(rolling_rocks, direction, free: list[list[bool]]):
    height, width = len(free), len(free[0])
    dx, dy = direction
    dir_idx = TILT_DIRECTIONS.index(direction)

    if dir_idx == 0:
        rolling_rocks = sorted(rolling_rocks, key=lambda pos: pos[1])
    elif dir_idx == 1:
        rolling_rocks = sorted(rolling_rocks, key=lambda pos: pos[0])
    elif dir_idx == 2:
        rolling_rocks = sorted(rolling_rocks, key=lambda pos: pos[1], reverse=True)
    elif dir_idx == 3:
        rolling_rocks = sorted(rolling_rocks, key=lambda pos: pos[0], reverse=True)

    for i in range(len(rolling_rocks)):
        rock_x, rock_y = rolling_rocks[i]
        new_rock_x, new_rock_y = rock_x, rock_y
        while (0 <= new_rock_x + dx < width and 0 <= new_rock_y + dy < height and
                free[new_rock_y+dy][new_rock_x+dx]):
            new_rock_x += dx
            new_rock_y += dy

        rolling_rocks[i] = (new_rock_x, new_rock_y)
        free[rock_y][rock_x] = True
        free[new_rock_y][new_rock_x] = False
    return rolling_rocks


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        map_rows = map_file.read().splitlines()

    rolling_rocks, static_rocks, free = parse_rock_map(map_rows)
    target_num_cycles = 1000000000
    rock_hashes = []
    cycles = 0
    skipped = False

    while cycles < target_num_cycles:
        for direction in TILT_DIRECTIONS:
            rolling_rocks = tilt(rolling_rocks, direction, free)

        cycles += 1
        rock_hash = hash(tuple(sorted(rolling_rocks)))

        if (not skipped and rock_hash in rock_hashes):
            cycle_length = cycles - rock_hashes.index(rock_hash) - 1
            num_skipped_cycles = (target_num_cycles - cycles) // cycle_length
            cycles += num_skipped_cycles * cycle_length
            skipped = True

        rock_hashes.append(rock_hash)

    load = calculate_load(rolling_rocks, len(map_rows))
    print(load)


if __name__ == '__main__':
    main()
