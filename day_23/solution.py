import sys
from enum import Enum
from collections import deque


class Direction(Enum):
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)
    W = (-1, 0)
    NW = (-1, -1)


DIRECTIONS = [d.value for d in list(Direction)]
ALL_DIRS = list(Direction)


def get_proposals(
        elf_positions: list[tuple[int]],
        directions: list[Direction]) -> dict[tuple[int], Direction]:

    proposals = {}
    for elf_x, elf_y in elf_positions:
        if any((elf_x+dx, elf_y+dy) in elf_positions for dx, dy in DIRECTIONS):

            for direction in directions:
                dir_idx = ALL_DIRS.index(direction)
                dirs = [ALL_DIRS[(dir_idx+i) % 8] for i in [-1, 0, 1]]

                if all((elf_x+dx, elf_y+dy) not in elf_positions
                       for dx, dy in [d.value for d in dirs]):

                    proposals[(elf_x, elf_y)] = direction
                    break

    return proposals


def get_destination(position, proposals):
    x, y = position
    dx, dy = proposals[position].value
    return x+dx, y+dy


def apply_proposals(
        proposals: dict[tuple[int], Direction],
        elf_positions: list[tuple[int]]):
    final_positions = list(elf_positions)

    for i, position in enumerate(elf_positions):
        if position in proposals:
            destination = get_destination(position, proposals)
            other_positions = elf_positions[0:i] + elf_positions[i+1:]
            other_destinations = [get_destination(p, proposals) for p in other_positions
                                  if p in proposals]

            if destination not in other_destinations:
                final_positions[i] = destination

    return final_positions


def print_positions(elf_positions):
    for row in range(12):
        for col in range(14):
            print('#' if (col, row) in elf_positions else '.', end='')
        print()
    print()


def main():
    filename = sys.argv[1]
    with open(filename) as grove_scan_file:
        grove_scan = grove_scan_file.read().splitlines()

    height = len(grove_scan)
    width = len(grove_scan[0])
    elf_positions = [(col, row) for row in range(height) for col in range(width)
                     if grove_scan[row][col] == '#']

    directions = deque([Direction.N, Direction.S, Direction.W, Direction.E])
    for _ in range(10):
        proposals = get_proposals(elf_positions, directions)
        elf_positions = apply_proposals(proposals, elf_positions)
        directions.rotate(-1)

    min_x = min(x for x, _ in elf_positions)
    max_x = max(x for x, _ in elf_positions)
    min_y = min(y for _, y in elf_positions)
    max_y = max(y for _, y in elf_positions)
    num_empty_tiles = 0

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x, y) not in elf_positions:
                num_empty_tiles += 1

    print(num_empty_tiles)


if __name__ == '__main__':
    main()
