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


def get_possible_moves(
        expedition_position: tuple[int],
        blizzards: list[Blizzard],
        valley_map: list[str]) -> list[tuple[int]]:

    moves = []
    next_blizzard_positions = {b.position for b in move_blizzards(blizzards, valley_map)}
    if expedition_position not in next_blizzard_positions:  # wait
        moves.append(expedition_position)

    current_blizzard_positions = {b.position for b in blizzards}
    x, y = expedition_position
    for dx, dy in MOVE_DELTAS:  # move
        if ((x+dx, y+dy) not in current_blizzard_positions | next_blizzard_positions
                and valley_map[y+dy][x+dx] != '#'):
            moves.append((x+dx, y+dy))

    return moves


def backtrack(
        expedition_position,
        blizzards, valley_map,
        goal_position,
        path,
        all_paths):

    possible_moves = get_possible_moves(expedition_position, blizzards, valley_map)
    if not possible_moves:
        return False

    for move in possible_moves:
        if move == goal_position:
            all_paths.append(path + [goal_position])
            return True
        result = backtrack(
            move,
            move_blizzards(blizzards, valley_map),
            valley_map,
            goal_position,
            path + [move],
            all_paths)
        if not result:
            break


def main():
    filename = sys.argv[1]
    with open(filename) as valley_map_file:
        valley_map = valley_map_file.read().splitlines()

    blizzards = get_blizzards(valley_map)
    expedition_position = (6, 3)
    goal_position = (6, 5)
    all_paths = []
    backtrack(
        expedition_position,
        blizzards,
        valley_map,
        goal_position,
        [],
        all_paths)
    a = 2


if __name__ == '__main__':
    main()
