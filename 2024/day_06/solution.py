import sys

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]


def find_guard(lab_map: list[str]) -> tuple[int]:
    height = len(lab_map)
    width = len(lab_map[0])
    return [(x, y) for x in range(width) for y in range(height) if
            lab_map[y][x] == '^'][0]


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        lab_map = map_file.read().splitlines()

    guard_start_pos = find_guard(lab_map)
    heading = 0
    height = len(lab_map)
    width = len(lab_map[0])
    guard_x, guard_y = guard_start_pos
    positions = set([guard_start_pos])

    while True:
        dx, dy = DIRECTIONS[heading]

        while (0 <= guard_x+dx < width and 0 <= guard_y+dy < height
               and lab_map[guard_y+dy][guard_x+dx] in '.^'):
            guard_x += dx
            guard_y += dy
            positions.add((guard_x, guard_y))

        if ((guard_x == 0 and heading == 3)
            or (guard_x == width-1 and heading == 1)
            or (guard_y == 0 and heading == 0)
                or (guard_y == height-1 and heading == 2)):
            break

        heading = (heading+1) % 4

    print(len(positions))


if __name__ == '__main__':
    main()
