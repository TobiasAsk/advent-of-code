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
        elf_positions: set[tuple[int]],
        directions: list[Direction]) -> dict[tuple[int], Direction]:

    proposals = {}
    for elf_x, elf_y in elf_positions:
        if any((elf_x+dx, elf_y+dy) in elf_positions for dx, dy in DIRECTIONS):

            for direction in directions:
                dir_idx = ALL_DIRS.index(direction)
                dirs = [ALL_DIRS[(dir_idx+i) % 8] for i in [-1, 0, 1]]

                if all((elf_x+dx, elf_y+dy) not in elf_positions
                       for dx, dy in [d.value for d in dirs]):

                    dx, dy = direction.value
                    proposals[(elf_x, elf_y)] = (elf_x+dx, elf_y+dy)
                    break

    return proposals


def apply_proposals(
        proposals: dict[tuple[int], tuple[int]],
        elf_positions: set[tuple[int]]):
    proposed_destinations = list(proposals.values())
    counts = {d: proposed_destinations.count(d) for d in proposed_destinations}
    return {proposals[p] if p in proposals and counts[proposals[p]] == 1
            else p for p in elf_positions}


def main():
    filename = sys.argv[1]
    with open(filename) as grove_scan_file:
        grove_scan = grove_scan_file.read().splitlines()

    height = len(grove_scan)
    width = len(grove_scan[0])
    elf_positions = set((col, row) for row in range(height) for col in range(width)
                        if grove_scan[row][col] == '#')

    previous_positions = set(elf_positions)
    directions = deque([Direction.N, Direction.S, Direction.W, Direction.E])
    num_rounds = 0

    while True:
        proposals = get_proposals(elf_positions, directions)
        elf_positions = apply_proposals(proposals, elf_positions)
        num_rounds += 1
        if previous_positions == elf_positions:
            break
        previous_positions = elf_positions
        directions.rotate(-1)

    print(num_rounds)


if __name__ == '__main__':
    main()
