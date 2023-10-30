import sys
from collections import namedtuple
from dataclasses import dataclass


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
    for blizzard in blizzards:
        new_position = get_new_position(blizzard, valley_map)

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


def get_blizzards(valley_map) -> frozenset[Blizzard]:
    blizzards = set()
    valley_height, valley_width = len(valley_map), len(valley_map[0])

    for row in range(valley_height):
        for col in range(valley_width):
            char = valley_map[row][col]

            if char in DIRECTIONS:
                blizzards.add(Blizzard(
                    position=(col, row),
                    direction=DIRECTIONS.index(char)))

    return frozenset(blizzards)


def get_new_position(
        blizzard: Blizzard,
        valley_map: list[str]) -> tuple[int]:

    x, y = blizzard.position
    dx, dy = MOVE_DELTAS[blizzard.direction]
    valley_height, valley_width = len(valley_map), len(valley_map[0])

    return ((x+dx, y+dy) if valley_map[y+dy][x+dx] != '#' else
            ((x+2*dx) % valley_width + dx, (y+2*dy) % valley_height + dy))


def get_possible_moves(
        expedition_position: tuple[int],
        blizzards: list[Blizzard],
        valley_map: list[str]) -> list[tuple[int]]:

    moves = []
    x, y = expedition_position
    next_blizzard_positions = {b.position for b in move_blizzards(blizzards, valley_map)}
    if expedition_position not in next_blizzard_positions and expedition_position != (1, 0):  # wait
        moves.append(expedition_position)

    for dx, dy in MOVE_DELTAS:  # move
        new_exp_pos = (x+dx, y+dy)
        # can loop around due to negative indexing but it's fine
        if valley_map[y+dy][x+dx] != '#' and new_exp_pos not in next_blizzard_positions:
            moves.append(new_exp_pos)

    return moves


@dataclass
class Search:
    shortest: int
    valley_map: list[str]

    def backtrack(
            self, expedition_position,
            blizzards,
            goal_position,
            minutes_spent=0):

        if minutes_spent < self.shortest:
            possible_moves = get_possible_moves(expedition_position, blizzards, self.valley_map)

            if goal_position in possible_moves:
                if minutes_spent + 1 < self.shortest:
                    self.shortest = minutes_spent + 1
                return

            for move in possible_moves:
                self.backtrack(
                    move,
                    move_blizzards(blizzards, self.valley_map),
                    goal_position,
                    minutes_spent+1)

def main():
    filename = sys.argv[1]
    with open(filename) as valley_map_file:
        valley_map = valley_map_file.read().splitlines()

    blizzards = get_blizzards(valley_map)
    expedition_position = (1, 0)
    # goal_position = (100, 36)
    goal_position = (6, 5)
    search = Search(valley_map=valley_map, shortest=100)
    search.backtrack(expedition_position, blizzards, goal_position)
    print(search.shortest)


if __name__ == '__main__':
    main()
