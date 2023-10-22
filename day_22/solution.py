import sys
from enum import Enum
from collections import namedtuple

FACE_SIZE = 50


class Direction(Enum):
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)


FoldCorner = namedtuple(
    'FoldCorner', ['face', 'clockwise_arm', 'counter_clockwise_arm'])

HIGHER_IS_HIGHER = [
    ['N/A', True, False, False],  # from right
    [True, 'N/A', False, False],  # from down
    [False, False, 'N/A', True],  # from left
    [False, False, True, 'N/A']  # from up
]


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
                corners.append(FoldCorner(
                    face=face,
                    clockwise_arm=other_dir,
                    counter_clockwise_arm=dir))

    return corners


def move_g(position, direction):
    return tuple(position[i]+direction[i] for i in range(2))


def rotate(direction: Direction, clockwise: bool) -> Direction:
    all_dirs = list(Direction)
    dir_idx = all_dirs.index(direction)
    offset = 1 if clockwise else -1
    return all_dirs[(dir_idx+offset) % len(all_dirs)]


def get_edge_pairs(
        corners: list[FoldCorner],
        faces: list[tuple[int]]) -> dict[tuple[tuple[int], Direction], tuple[tuple[int], Direction]]:

    pairs = {}

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
                    counter_clockwise_dir = rotate(counter_clockwise_dir, False)
                    counter_clockwise_edge = rotate(counter_clockwise_edge, False)

            if new_counter_clockwise_pos in faces:
                counter_clockwise_pos = new_counter_clockwise_pos
                keep_going = True

                if not new_clockwise_pos in faces:
                    clockwise_dir = rotate(clockwise_dir, True)
                    clockwise_edge = rotate(clockwise_edge, True)

            if keep_going:
                clockwise_dir_idx = list(Direction).index(clockwise_dir)
                counter_clockwise_dir_idx = list(Direction).index(counter_clockwise_dir)
                higher_is_higher = HIGHER_IS_HIGHER[clockwise_dir_idx][counter_clockwise_dir_idx]

                pairs[(clockwise_pos, clockwise_edge)] = (counter_clockwise_pos,
                                                          rotate(rotate(counter_clockwise_edge, True), True),
                                                          higher_is_higher)
                pairs[(counter_clockwise_pos, counter_clockwise_edge)] = (clockwise_pos,
                                                                          rotate(rotate(clockwise_edge, True), True),
                                                                          higher_is_higher)

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


def move(
        num_steps: int,
        facing: int,
        position: tuple[int],
        board_map: list[str],
        pairs: dict) -> tuple[tuple[int], int]:

    max_width, max_height = len(board_map[0]), len(board_map)
    x, y = position

    for _ in range(num_steps):
        d_x, d_y = list(Direction)[facing].value
        new_x = x + d_x
        new_y = y + d_y
        wrap = False
        face = x // FACE_SIZE, y // FACE_SIZE

        if (0 <= new_x < max_width and 0 <= new_y < max_height):
            if board_map[new_y][new_x] == '.':
                x = new_x
                y = new_y

            elif board_map[new_y][new_x] == ' ':
                wrap = True

        else:
            wrap = True

        if wrap:
            direction = list(Direction)[facing]
            (new_face_x, new_face_y), new_direction, higher_is_higher = pairs[(face, direction)]

            if new_direction in [Direction.DOWN, Direction.UP]:
                new_y = (new_face_y * FACE_SIZE if new_direction ==
                         Direction.DOWN else new_face_y * FACE_SIZE + FACE_SIZE - 1)
                dimension = x if direction in [Direction.DOWN, Direction.UP] else y
                factor = (dimension % FACE_SIZE) if higher_is_higher else FACE_SIZE - dimension % FACE_SIZE - 1
                new_x = new_face_x * FACE_SIZE + factor

            else:
                new_x = (new_face_x * FACE_SIZE if new_direction ==
                         Direction.RIGHT else new_face_x * FACE_SIZE + FACE_SIZE - 1)
                dimension = y if direction in [Direction.RIGHT, Direction.LEFT] else x
                factor = (dimension % FACE_SIZE) if higher_is_higher else FACE_SIZE - dimension % FACE_SIZE - 1
                new_y = new_face_y * FACE_SIZE + factor

            if board_map[new_y][new_x] == '.':
                x = new_x
                y = new_y
                facing = list(Direction).index(new_direction)

        position = (x, y)

    return position, facing


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        notes = map_file.read().splitlines()

    board_map, path, position = parse_notes(notes)
    facing = 0

    faces = get_faces(board_map)
    corners = get_corners(faces)
    edge_pairs = get_edge_pairs(corners, faces)

    for instruction in path:
        if isinstance(instruction, int):
            position, facing = move(instruction, facing, position, board_map, edge_pairs)

        else:
            rotation = 1 if instruction == 'R' else -1
            facing = (facing + rotation) % 4

    x, y = position
    password = 1000 * (y+1) + 4 * (x+1) + facing
    print(f'Password is {password}')


if __name__ == '__main__':
    main()
