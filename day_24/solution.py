import sys
from collections import namedtuple

Blizzard = namedtuple('blizzard', ['position', 'direction'])
DIRECTIONS = '>v<^'
MOVE_DELTAS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def move_blizzards(
        blizzards: list[Blizzard],
        valley_map: list[str]) -> list[Blizzard]:

    moved: list[Blizzard] = []
    valley_height, valley_width = len(valley_map), len(valley_map[0])

    for blizzard in blizzards:
        x, y = blizzard.position
        dx, dy = MOVE_DELTAS[blizzard.direction]
        new_position = ((x+dx, y+dy) if valley_map[y+dy][x+dx] != '#' else
                        ((x+2*dx) % valley_width + dx, (y+2*dy) % valley_height + dy))

        moved.append(Blizzard(
            position=new_position,
            direction=blizzard.direction))

    return moved


def print_map(blizzards: list[Blizzard], valley_map):
    valley_height, valley_width = len(valley_map), len(valley_map[0])
    blizzard_positions = [b.position for b in blizzards]

    for row in range(valley_height):
        for col in range(valley_width):
            if (col, row) in blizzard_positions:
                blizzard = next(b for b in blizzards if b.position == (col, row))
                print(DIRECTIONS[blizzard.direction], end='')
            else:
                print('#' if col in [0, valley_width-1]
                      or row in [0, valley_height-1] else '.', end='')
        print()


def get_blizzards(valley_map) -> list[Blizzard]:
    blizzards = []
    valley_height, valley_width = len(valley_map), len(valley_map[0])

    for row in range(valley_height):
        for col in range(valley_width):
            char = valley_map[row][col]

            if char in DIRECTIONS:
                blizzards.append(Blizzard(
                    position=(col, row),
                    direction=DIRECTIONS.index(char)))

    return blizzards


def main():
    filename = sys.argv[1]
    with open(filename) as valley_map_file:
        valley_map = valley_map_file.read().splitlines()

    blizzards = get_blizzards(valley_map)
    for _ in range(5):
        blizzards = move_blizzards(blizzards, valley_map)
        print_map(blizzards, valley_map)


if __name__ == '__main__':
    main()
