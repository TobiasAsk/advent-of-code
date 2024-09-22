import sys
from functools import cache, reduce
from collections import defaultdict

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]


class GardenMap:
    def __init__(self, map_lines):
        self.map_lines = map_lines
        self.width = len(map_lines[0])
        self.height = len(map_lines)
        self.starting_position = [(x, y) for y in range(self.height) for x in range(self.width) if
                                  self.map_lines[y][x] == 'S'][0]
        self.seen_at_steps = defaultdict(set)

    @cache
    def get_num_plots_within_reach(
            self, position: tuple[int],
            num_remaining_steps: int) -> frozenset[tuple[int]]:

        if num_remaining_steps == 0:
            return 1

        x, y = position
        available_plots = []
        for dx, dy in DIRECTIONS:
            if (0 <= x+dx < self.width and 0 <= y+dy < self.height and
                    self.map_lines[y+dy][x+dx] in ['.', 'S']) and not (x+dx, y+dy) in self.seen_at_steps[num_remaining_steps-1]:

                self.seen_at_steps[num_remaining_steps-1].add((x+dx, y+dy))
                available_plots.append((x+dx, y+dy))

        return sum(self.get_num_plots_within_reach(p, num_remaining_steps-1)
                   for p in available_plots)


def main():
    filename = sys.argv[1]
    with open(filename) as garden_map_file:
        garden_map = GardenMap(garden_map_file.read().splitlines())

    num_plots_within_reach = garden_map.get_num_plots_within_reach(garden_map.starting_position, 64)
    print(num_plots_within_reach)


if __name__ == '__main__':
    main()
