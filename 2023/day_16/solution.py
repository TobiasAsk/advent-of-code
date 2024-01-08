import sys

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

REFLECTIONS = {
    (1, 0): {
        '\\': (0, 1),
        '/': (0, -1),
        '.': (1, 0),
        '-': (1, 0),
        '|': ((0, -1), (0, 1))
    },
    (0, 1): {
        '\\': (1, 0),
        '/': (-1, 0),
        '.': (0, 1),
        '-': ((1, 0), (-1, 0)),
        '|': (0, 1)
    },
    (-1, 0): {
        '\\': (0, -1),
        '/': (0, 1),
        '.': (-1, 0),
        '-': (-1, 0),
        '|': ((0, -1), (0, 1))
    },
    (0, -1): {
        '\\': (-1, 0),
        '/': (1, 0),
        '.': (0, -1),
        '-': ((1, 0), (-1, 0)),
        '|': (0, -1)
    }
}


def get_new_direction(direction: tuple[int], tile: str) -> tuple[tuple[int], bool]:
    new_dir = REFLECTIONS[direction][tile]
    if isinstance(new_dir[0], int):
        return new_dir, False
    else:
        return new_dir, True


def get_num_energized_tiles(start_position, start_direction, contraption_layout):
    height, width = len(contraption_layout), len(contraption_layout[0])
    energized_tiles = {start_position}
    beam_starts = set()
    beams = [(start_position, start_direction)]

    while beams:
        position, direction = beams.pop()
        beam_starts.add((position, direction))
        x, y = position
        dx, dy = direction
        split = False

        while 0 <= x < width and 0 <= y < height and not split:
            energized_tiles.add((x, y))
            new_direction, split = get_new_direction((dx, dy), contraption_layout[y][x])
            if split:
                beams.extend(((x+split_dir[0], y+split_dir[1]), split_dir) for split_dir in new_direction
                             if ((x+split_dir[0], y+split_dir[1]), split_dir) not in beam_starts)
            else:
                dx, dy = new_direction
                x += dx
                y += dy

    return len(energized_tiles)


def main():
    filename = sys.argv[1]
    with open(filename) as contraption_layout_file:
        contraption_layout = contraption_layout_file.read().splitlines()

    height, width = len(contraption_layout), len(contraption_layout[0])
    max_num_energized_tiles = 0

    for x in range(width):
        for y, dy in [(0, 1), (height-1, -1)]:
            start_position = (x, y)
            start_direction = (0, dy)
            num_energized = get_num_energized_tiles(start_position, start_direction, contraption_layout)
            max_num_energized_tiles = max(max_num_energized_tiles, num_energized)

    for y in range(height):
        for x, dx in [(0, 1), (width-1, -1)]:
            start_position = (x, y)
            start_direction = (dx, 0)
            num_energized = get_num_energized_tiles(start_position, start_direction, contraption_layout)
            max_num_energized_tiles = max(max_num_energized_tiles, num_energized)

    print(max_num_energized_tiles)


if __name__ == '__main__':
    main()
