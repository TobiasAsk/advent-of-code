import sys
from enum import Enum
from collections import namedtuple

FACE_SIZE = 4


class Direction(Enum):
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)


FoldCorner = namedtuple(
    'FoldCorner', ['face', 'clockwise_arm', 'counter_clockwise_arm'])


CORNERS = [
    (Direction.UP, Direction.RIGHT),
    (Direction.RIGHT, Direction.DOWN),
    (Direction.DOWN, Direction.LEFT),
    (Direction.LEFT, Direction.UP),
]


def get_faces(board_map: list[str]) -> list[tuple[int]]:
    max_width = len(board_map[0])
    max_height = len(board_map)
    faces = []

    for row in range(0, max_height, FACE_SIZE):
        for col in range(0, max_width, FACE_SIZE):
            if board_map[row][col] != ' ':
                faces.append((col//FACE_SIZE, row//FACE_SIZE))
    return faces


def get_corners(faces: list[tuple[int]]) -> list[FoldCorner]:
    corners = []
    for face in faces:
        x, y = face
        for dir, other_dir in CORNERS:
            first_point = x+dir.value[0], y+dir.value[1]
            second_point = x+other_dir.value[0], y+other_dir.value[1]

            if first_point in faces and second_point in faces:
                corners.append(
                    FoldCorner(
                        face=face,
                        clockwise_arm=other_dir,
                        counter_clockwise_arm=dir))

    return corners


def move_g(position, direction):
    return tuple(position[i]+direction[i] for i in range(2))


def get_edge_pairs(corners: list[FoldCorner], faces: list[tuple[int]]):
    pairs = []

    for corner in corners:
        clockwise_pos: tuple[int] = corner.face
        clockwise_dir: Direction = corner.clockwise_arm
        clockwise_edge: Direction = corner.counter_clockwise_arm

        counter_clockwise_pos = corner.face
        counter_clockwise_dir: Direction = corner.counter_clockwise_arm
        counter_clockwise_edge: Direction = corner.clockwise_arm

        keep_going = True
        while keep_going:
            keep_going = False
            new_clockwise_pos = move_g(clockwise_pos, clockwise_dir.value)
            new_counter_clockwise_pos = move_g(
                counter_clockwise_pos, counter_clockwise_dir.value)

            if new_clockwise_pos in faces:
                clockwise_pos = new_clockwise_pos
                keep_going = True

                if not new_counter_clockwise_pos in faces:
                    all_dirs = list(Direction)
                    edge_idx = all_dirs.index(counter_clockwise_edge)
                    dir_idx = all_dirs.index(counter_clockwise_dir)
                    counter_clockwise_dir = all_dirs[(
                        dir_idx-1) % len(all_dirs)]
                    counter_clockwise_edge = all_dirs[(
                        edge_idx-1) % len(all_dirs)]

            if new_counter_clockwise_pos in faces:
                counter_clockwise_pos = new_counter_clockwise_pos
                keep_going = True

                if not new_clockwise_pos in faces:
                    all_dirs = list(Direction)
                    edge_idx = all_dirs.index(clockwise_edge)
                    dir_idx = all_dirs.index(clockwise_dir)
                    clockwise_dir = all_dirs[(
                        dir_idx+1) % len(all_dirs)]
                    clockwise_edge = all_dirs[(
                        edge_idx+1) % len(all_dirs)]

            if keep_going:
                pairs.append(
                    ((clockwise_pos, clockwise_edge),
                        (counter_clockwise_pos, counter_clockwise_edge))
                )

    return pairs


def parse_notes(notes):
    max_width = 0
    board_map = []

    for row in notes[:-2]:
        board_map.append(row)
        max_width = max(max_width, len(row))

    board_map = [row if len(row) == max_width else row +
                 ' ' * (max_width-len(row)) for row in board_map]

    raw_path: str = notes[-1]
    path = []
    i = 0

    while i < len(raw_path):
        if raw_path[i].isdigit():
            digit_start = i
            while i < len(raw_path) and raw_path[i].isdigit():
                i += 1
            path.append(int(raw_path[digit_start:i]))
        else:
            path.append(raw_path[i])
            i += 1

    start_x = [i for i in range(len(board_map[0]))
               if board_map[0][i] == '.'][0]
    return board_map, path, (start_x, 0)


def print_board(board_map, position):
    x, y = position
    for row in range(len(board_map)):
        out_row = ''.join(['P' if i == x and row == y else board_map[row][i]
                           for i in range(len(board_map[row]))])
        print(out_row)
    print()


def move(num_steps, facing, position, board_map) -> int:
    max_width, max_height = len(board_map[0]), len(board_map)
    d_x, d_y = list(Direction)[facing].value
    x, y = position

    for _ in range(num_steps):
        new_x = x + d_x
        new_y = y + d_y
        wrap = False

        if (0 <= new_x < max_width and 0 <= new_y < max_height):
            if board_map[new_y][new_x] == '.':
                x = new_x
                y = new_y

            elif board_map[new_y][new_x] == ' ':
                wrap = True

        else:
            wrap = True

        if wrap:
            opposite_d_x, opposite_d_y = list(Direction)[(facing+2) % 4].value

            while (0 <= new_x + opposite_d_x < max_width and 0 <= new_y + opposite_d_y < max_height and
                    board_map[new_y+opposite_d_y][new_x+opposite_d_x] != ' '):
                new_x += opposite_d_x
                new_y += opposite_d_y

            if board_map[new_y][new_x] == '.':
                x = new_x
                y = new_y
            else:
                break

        position = (x, y)

    return position


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        notes = map_file.read().splitlines()

    board_map, path, position = parse_notes(notes)
    facing = 0

    for instruction in path:
        if isinstance(instruction, int):
            position = move(instruction, facing, position, board_map)

        else:
            rotation = 1 if instruction == 'R' else -1
            facing = (facing + rotation) % 4

    x, y = position
    password = 1000 * (y+1) + 4 * (x+1) + facing
    print(f'Password is {password}')

    faces = get_faces(board_map)
    corners = get_corners(faces)
    edge_pairs = get_edge_pairs(corners, faces)
    a = 2


if __name__ == '__main__':
    f = Direction.LEFT
    main()
