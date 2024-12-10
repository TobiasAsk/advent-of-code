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


def get_positions(lab_map: list[str], guard_start_pos: tuple[int]) -> set[tuple[int]]:
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

    return positions


def is_loop_walk(guard_start_pos, lab_map) -> bool:
    heading = 0
    height = len(lab_map)
    width = len(lab_map[0])
    guard_x, guard_y = guard_start_pos
    corners = set()

    while True:
        dx, dy = DIRECTIONS[heading]

        while (0 <= guard_x+dx < width and 0 <= guard_y+dy < height
               and lab_map[guard_y+dy][guard_x+dx] in '.^'):
            guard_x += dx
            guard_y += dy

        if ((guard_x == 0 and heading == 3)
            or (guard_x == width-1 and heading == 1)
            or (guard_y == 0 and heading == 0)
                or (guard_y == height-1 and heading == 2)):
            return False

        if (guard_x, guard_y, heading) in corners:
            return True
        corners.add((guard_x, guard_y, heading))

        heading = (heading+1) % 4


def print_map(lab_map):
    for row in lab_map:
        print(''.join(t for t in row))


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        lab_map = map_file.read().splitlines()

    guard_start_pos = find_guard(lab_map)
    positions = get_positions(lab_map, guard_start_pos)

    height = len(lab_map)
    width = len(lab_map[0])

    obstacle_coords = [(x, y) for x in range(width) for y in range(height) if
                       lab_map[y][x] == '#']
    obstacle_x_coords = set(x for x, _ in obstacle_coords)
    obstacle_y_coords = set(y for _, y in obstacle_coords)
    num_options = 0
    for x, y in positions - {guard_start_pos}:
        if x in obstacle_x_coords or y in obstacle_y_coords:
            old_row = lab_map[y]
            lab_map[y] = old_row[:x] + '#' + old_row[x+1:]
            if is_loop_walk(guard_start_pos, lab_map):
                num_options += 1
            lab_map[y] = old_row

    print(num_options)


if __name__ == '__main__':
    main()
