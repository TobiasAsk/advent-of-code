'''Nice twist in part two. I kept the box representation as single points, and handled the width
in the computations. They're hard-coded to a width of 2, though, which would quickly become messy
for wider boxes. Perhaps a representation of single points together with an on-demand expanded
representation of all coordinates with boxes would be best in general, but it would be more costly.

Move algorithm: flood-fill from robot position to get all boxes affected by a move, then do
collision detection with the wall.
'''

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
    return {(2*x, y) for x in range(width) for y in range(height) if
            warehouse_map[y][x] == object}


def get_robot_position(warehouse_map: list[str]) -> tuple[int]:
    return next(iter(get_object_positions(warehouse_map, '@')))


def get_box_positions(warehouse_map):
    return get_object_positions(warehouse_map, 'O')


def get_wall_positions(warehouse_map):
    width, height = len(warehouse_map[0]), len(warehouse_map)
    extended = {(2*x, y) for x in range(width) for y in range(height) if
                warehouse_map[y][x] == '#'}
    added_positions = {(2*x+1, y) for x in range(width) for y in range(height) if
                       warehouse_map[y][x] == '#'}

    return extended | added_positions


def get_connected_boxes(direction, robot_pos, box_positions) -> set[tuple[int]]:
    dx, dy = direction
    boxes = set()
    queue = [robot_pos]
    visited = set()

    while queue:
        x, y = queue.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) in box_positions:
            boxes.add((x, y))
        if (x+dx, y+dy) in box_positions:
            queue.append((x+dx, y+dy))
        if (x+dx-1, y+dy) in box_positions:
            queue.append((x+dx-1, y+dy))
        if (x, y) != robot_pos and (x+dx+1, y+dy) in box_positions:
            queue.append((x+dx+1, y+dy))

    return boxes


def move_objects(
        direction: tuple[int],
        robot_pos: tuple[int],
        box_positions: set[tuple[int]],
        wall_positions: set[tuple[int]]):

    dx, dy = direction
    boxes_to_move = get_connected_boxes(direction, robot_pos, box_positions)
    new_box_positions = box_positions
    new_robot_position = robot_pos

    if boxes_to_move:
        # simple collision detection: move boxes and check if any of them
        # are in the wall
        moved_box_positions = {(x+dx, y+dy) for (x, y) in boxes_to_move}
        if all((x, y) not in wall_positions and (x+1, y) not in wall_positions
               for (x, y) in moved_box_positions):
            new_robot_position = robot_pos[0]+dx, robot_pos[1]+dy
            new_box_positions = moved_box_positions | (box_positions - boxes_to_move)
    else:
        moved_robot_position = robot_pos[0]+dx, robot_pos[1]+dy
        if moved_robot_position not in wall_positions:
            new_robot_position = moved_robot_position

    return new_robot_position, new_box_positions


def print_state(robot_pos, box_positions, wall_positions, bounds):
    width, height = bounds
    for y in range(height):
        print(''.join('#' if (x, y) in wall_positions else
                      '[' if (x, y) in box_positions else
                      ']' if (x-1, y) in box_positions else
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
    # print_state(robot_pos, box_positions, wall_positions, (2*width, height))

    # while True:
    #     input_move = input()
    #     robot_pos, box_positions = move_objects(MOVES[input_move], robot_pos, box_positions, wall_positions)
    #     print()
    #     print_state(robot_pos, box_positions, wall_positions, (2*width, height))

    for move in movements:
        robot_pos, box_positions = move_objects(MOVES[move], robot_pos, box_positions, wall_positions)
        # print()
        # print(move)
        # print_state(robot_pos, box_positions, wall_positions, (2*width, height))

    print(sum(gps_coordinate(b) for b in box_positions))


if __name__ == '__main__':
    main()
