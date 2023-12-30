import sys


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
        print(''.join('O' if (x, y) in rolling_rocks else '.' for x in range(width)))


def calculate_load(rolling_rocks, platform_height):
    def load(rock_y): return platform_height - rock_y
    return sum(load(y) for _, y in rolling_rocks)


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        rolling_rocks, static_rocks, dimensions = parse_rock_map(map_file.readlines())

    moving = True
    while moving:
        moving = False
        for i in range(len(rolling_rocks)):
            rock_x, rock_y = rolling_rocks[i]
            if rock_y - 1 >= 0 and (rock_x, rock_y-1) not in rolling_rocks + static_rocks:
                rolling_rocks[i] = (rock_x, rock_y-1)
                moving = True

    load = calculate_load(rolling_rocks, dimensions[0])
    print(load)


if __name__ == '__main__':
    main()
