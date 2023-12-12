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

START_REPLACEMENTS = {
    (MovementDirection.SOUTH, MovementDirection.EAST): Bend.SOUTH_WEST.value,
    (MovementDirection.SOUTH, MovementDirection.WEST): Bend.SOUTH_EAST.value,
    (MovementDirection.NORTH, MovementDirection.WEST): Bend.NORTH_EAST.value,
    (MovementDirection.NORTH, MovementDirection.EAST): Bend.NORTH_WEST.value,
    (MovementDirection.EAST, MovementDirection.SOUTH): Bend.NORTH_EAST.value,
    (MovementDirection.NORTH, MovementDirection.NORTH): Bend.STRAIGHT_VERTICAL.value,
    (MovementDirection.SOUTH, MovementDirection.SOUTH): Bend.STRAIGHT_VERTICAL.value,
    (MovementDirection.WEST, MovementDirection.WEST): Bend.STRAIGHT_HORIZONTAL.value,
    (MovementDirection.EAST, MovementDirection.EAST): Bend.STRAIGHT_HORIZONTAL.value,
}

CORNERS = 'F7JL'


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


def get_loop_info(start_pos, first_dir, start_dir, pipe_map) -> tuple[str, set[tuple[int]]]:
    position = start_pos
    direction = start_dir
    loop_tiles = {position}

    while pipe_map[position[1]][position[0]] != 'S':
        last_direction = direction
        position, direction = move(position, direction, pipe_map)
        loop_tiles.add(position)

    start_replacement = START_REPLACEMENTS[(last_direction, first_dir)]
    return start_replacement, loop_tiles


def ray_cast(row, pipe_map, loop_tiles):
    # Outside: even
    # Inside: odd
    width = len(pipe_map[0])
    num_intersections = [0 for _ in range(width)]
    intersection_count = 0
    first_corner = None

    for x in range(width):
        num_intersections[x] = intersection_count

        if (x, row) in loop_tiles:
            if pipe_map[row][x] == '|':
                intersection_count += 1
            elif pipe_map[row][x] in CORNERS:
                if (first_corner == 'F' and pipe_map[row][x] == 'J') or (first_corner == 'L' and pipe_map[row][x] == '7'):
                    intersection_count += 1
                first_corner = pipe_map[row][x]

    return num_intersections


def main():
    filename = sys.argv[1]
    with open(filename) as pipe_map_file:
        pipe_map = pipe_map_file.read().splitlines()

    start_pos = get_starting_position(pipe_map)
    start_direction = get_starting_direction(start_pos, pipe_map)
    position, direction = move(start_pos, start_direction, pipe_map)
    height, width = len(pipe_map), len(pipe_map[0])

    start_replacement, loop_tiles = get_loop_info(position, start_direction, direction, pipe_map)
    _, start_y = start_pos
    pipe_map[start_y] = pipe_map[start_y].replace('S', start_replacement)

    intersections = [ray_cast(row, pipe_map, loop_tiles) for row in range(height)]
    enclosed_tiles = [(x, y) for y in range(height) for x in range(width)
                      if (x, y) not in loop_tiles and intersections[y][x] % 2 == 1]

    print(len(enclosed_tiles))


if __name__ == '__main__':
    main()
