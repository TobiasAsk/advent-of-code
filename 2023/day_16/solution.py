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


def main():
    filename = sys.argv[1]
    with open(filename) as contraption_layout_file:
        contraption_layout = contraption_layout_file.read().splitlines()

    height, width = len(contraption_layout), len(contraption_layout[0])
    start_position = (0, 0)
    start_direction = (1, 0)

    if contraption_layout[0][0] != '.':
        start_direction, _ = get_new_direction(start_direction, contraption_layout[0][0])

    energized_tiles = {start_position}
    beam_starts = set()
    beams = [(start_position, start_direction)]

    while beams:
        position, direction = beams.pop()
        beam_starts.add((position, direction))
        dx, dy = direction
        x, y = position
        split = False

        while 0 <= x+dx < width and 0 <= y+dy < height and not split:
            x += dx
            y += dy
            energized_tiles.add((x, y))

            tile = contraption_layout[y][x]
            new_direction, split = get_new_direction((dx, dy), tile)

            if split:
                beams.extend(((x, y), split_dir) for split_dir in new_direction
                             if ((x, y), split_dir) not in beam_starts)
            else:
                dx, dy = new_direction

    print(len(energized_tiles))


if __name__ == '__main__':
    main()
