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


def main():
    filename = sys.argv[1]
    with open(filename) as pipe_map_file:
        pipe_map = pipe_map_file.read().splitlines()

    start_pos = get_starting_position(pipe_map)
    start_direction = get_starting_direction(start_pos, pipe_map)
    position, direction = move(start_pos, start_direction, pipe_map)
    loop_length = 1

    while pipe_map[position[1]][position[0]] != 'S':
        position, direction = move(position, direction, pipe_map)
        loop_length += 1

    print(loop_length // 2)


if __name__ == '__main__':
    main()
