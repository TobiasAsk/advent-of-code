import sys
from enum import Enum


class MovementDirection(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


class Bend(Enum):
    SOUTH_WEST = 'L'
    SOUTH_EAST = 'J'
    NORTH_EAST = '7'
    NORTH_WEST = 'F'
    STRAIGHT_VERTICAL = '|'
    STRAIGHT_HORIZONTAL = '-'


PIPE_TURNS = {
    MovementDirection.EAST: {
        Bend.STRAIGHT_HORIZONTAL.value: MovementDirection.EAST,
        Bend.SOUTH_EAST.value: MovementDirection.NORTH,
        Bend.NORTH_EAST.value: MovementDirection.SOUTH
    },
    MovementDirection.SOUTH: {
        Bend.STRAIGHT_VERTICAL.value: MovementDirection.SOUTH,
        Bend.SOUTH_EAST.value: MovementDirection.WEST,
        Bend.SOUTH_WEST.value: MovementDirection.EAST
    },
    MovementDirection.WEST: {
        Bend.STRAIGHT_HORIZONTAL.value: MovementDirection.WEST,
        Bend.SOUTH_WEST.value: MovementDirection.NORTH,
        Bend.NORTH_WEST.value: MovementDirection.SOUTH
    },
    MovementDirection.NORTH: {
        Bend.STRAIGHT_VERTICAL.value: MovementDirection.NORTH,
        Bend.NORTH_EAST.value: MovementDirection.WEST,
        Bend.NORTH_WEST.value: MovementDirection.EAST
    }
}


def get_starting_direction(start_pos, pipe_map):
    start_x, start_y = start_pos
    height, width = len(pipe_map), len(pipe_map[0])

    for direction in list(MovementDirection):
        dx, dy = direction.value
        if 0 <= start_y + dy < height and 0 <= start_x + dx < width:
            next_tile = pipe_map[start_y+dy][start_x+dx]
            if next_tile in PIPE_TURNS[direction]:
                return direction


def get_starting_position(pipe_map: list[str]) -> tuple[int]:
    height, width = len(pipe_map), len(pipe_map[0])
    return [(x, y) for y in range(height) for x in range(width)
            if pipe_map[y][x] == 'S'][0]


def move(position: tuple[int],
         direction: MovementDirection,
         pipe_map: list[str]) -> tuple[tuple[int], MovementDirection]:

    dx, dy = direction.value
    x, y = position
    x += dx
    y += dy
    tile = pipe_map[y][x]
    direction = PIPE_TURNS[direction].get(tile)
    return (x, y), direction


def rotate(direction: MovementDirection, clockwise: bool) -> MovementDirection:
    all_dirs = list(MovementDirection)
    dir_idx = all_dirs.index(direction)
    offset = 1 if clockwise else -1
    return all_dirs[(dir_idx+offset) % len(all_dirs)]


def flood_fill(
        position: tuple[int],
        pipe_map: list[str],
        loop_tiles: set[tuple[int]]) -> set[tuple[int]]:
    q = [position]
    tiles = set()
    height, width = len(pipe_map), len(pipe_map[0])

    while q:
        x, y = q.pop()
        if (x, y) not in tiles:
            tiles.add((x, y))

            for direction in list(MovementDirection):
                dx, dy = direction.value
                if (0 <= y+dy < height and 0 <= x+dx < width and
                        (x+dx, y+dy) not in loop_tiles and (x+dx, y+dy) not in tiles):
                    q.append((x+dx, y+dy))

    return tiles


def get_loop_info(start_pos, start_dir, pipe_map) -> tuple[bool, set[tuple[int]]]:
    position = start_pos
    direction = start_dir
    turn_sum = 0
    all_dirs = list(MovementDirection)
    loop_tiles = {position}

    while pipe_map[position[1]][position[0]] != 'S':
        previous_direction = direction
        position, direction = move(position, direction, pipe_map)
        if direction != previous_direction:
            prev_dir_idx = all_dirs.index(previous_direction)
            turn_diff = 1 if all_dirs[(prev_dir_idx+1) % 4] == direction else -1
            turn_sum += turn_diff
        loop_tiles.add(position)

    return turn_sum > 0, loop_tiles


def main():
    filename = sys.argv[1]
    with open(filename) as pipe_map_file:
        pipe_map = pipe_map_file.read().splitlines()

    start_pos = get_starting_position(pipe_map)
    start_direction = get_starting_direction(start_pos, pipe_map)
    position, direction = move(start_pos, start_direction, pipe_map)
    height, width = len(pipe_map), len(pipe_map[0])

    is_clockwise, loop_tiles = get_loop_info(position, direction, pipe_map)
    enclosed_tiles = set()

    while pipe_map[position[1]][position[0]] != 'S':
        inside_dir = rotate(direction, clockwise=is_clockwise)
        x, y = position
        rhs_dx, rhs_dy = inside_dir.value
        within_bounds = 0 <= y+rhs_dy < height and 0 <= x+rhs_dx < width

        if (within_bounds and (x+rhs_dx, y+rhs_dy) not in loop_tiles
                and (x+rhs_dx, y+rhs_dy) not in enclosed_tiles):
            tiles_in_segment = flood_fill((x+rhs_dx, y+rhs_dy), pipe_map, loop_tiles)
            enclosed_tiles |= tiles_in_segment

        position, direction = move(position, direction, pipe_map)

    print(len(enclosed_tiles))


if __name__ == '__main__':
    main()
