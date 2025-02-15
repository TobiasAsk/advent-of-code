import sys

MOVES = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1)
}


def parse(warehouse_map_and_movements: str) -> tuple[list[str], str]:
    warehouse_map, movements = warehouse_map_and_movements.split('\n\n')
    return warehouse_map.splitlines(), ''.join(l for l in movements.splitlines())


def get_object_positions(warehouse_map: list[str], object: str) -> set[tuple[int]]:
    width, height = len(warehouse_map[0]), len(warehouse_map)
    return {(x, y) for x in range(width) for y in range(height) if
            warehouse_map[y][x] == object}


def get_robot_position(warehouse_map: list[str]) -> tuple[int]:
    return next(iter(get_object_positions(warehouse_map, '@')))


def get_box_positions(warehouse_map):
    return get_object_positions(warehouse_map, 'O')


def get_wall_positions(warehouse_map):
    return get_object_positions(warehouse_map, '#')


def move_objects(move, robot_pos, box_positions, wall_positions):
    dx, dy = move
    x, y = robot_pos
    boxes_to_move: set[tuple[int]] = set()
    while (x+dx, y+dy) in box_positions:
        x += dx
        y += dy
        boxes_to_move.add((x, y))

    new_robot_pos = robot_pos
    new_box_positions = box_positions

    if (x+dx, y+dy) not in wall_positions | box_positions:
        new_robot_pos = (robot_pos[0]+dx, robot_pos[1]+dy)

        new_box_positions = {box_pos if box_pos not in boxes_to_move else (box_pos[0]+dx, box_pos[1]+dy)
                             for box_pos in box_positions}

    return new_robot_pos, new_box_positions


def print_state(robot_pos, box_positions, wall_positions, bounds):
    width, height = bounds
    for y in range(height):
        print(''.join('#' if (x, y) in wall_positions else
                      'O' if (x, y) in box_positions else
                      '@' if (x, y) == robot_pos else
                      '.' for x in range(width)))


def gps_coordinate(box_pos):
    return box_pos[0] + 100*box_pos[1]


def main():
    filename = sys.argv[1]
    with open(filename) as warehouse_map_and_movements_file:
        warehouse_map, movements = parse(warehouse_map_and_movements_file.read())

    robot_pos = get_robot_position(warehouse_map)
    box_positions = get_box_positions(warehouse_map)
    wall_positions = get_wall_positions(warehouse_map)
    width, height = len(warehouse_map[0]), len(warehouse_map)

    # print_state(robot_pos, box_positions, wall_positions, (width, height))
    for move in movements:
        robot_pos, box_positions = move_objects(MOVES[move], robot_pos, box_positions, wall_positions)
        # print()
        # print(move)
        # print_state(robot_pos, box_positions, wall_positions, (width, height))

    print(sum(gps_coordinate(b) for b in box_positions))


if __name__ == '__main__':
    main()
