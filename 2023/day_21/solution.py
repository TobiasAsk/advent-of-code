import sys
from functools import cache, reduce

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

    @cache
    def get_plots_within_reach(
            self, position: tuple[int],
            num_remaining_steps: int) -> frozenset[tuple[int]]:

        if num_remaining_steps == 0:
            return frozenset([position])

        x, y = position
        available_plots = []
        for dx, dy in DIRECTIONS:
            if (0 <= x+dx < self.width and 0 <= y+dy < self.height and
                    self.map_lines[y+dy][x+dx] in ['.', 'S']):
                available_plots.append((x+dx, y+dy))

        return reduce(lambda a, b: a | b, (self.get_plots_within_reach(p, num_remaining_steps-1)
                      for p in available_plots))


def main():
    filename = sys.argv[1]
    with open(filename) as garden_map_file:
        garden_map = GardenMap(garden_map_file.read().splitlines())

    plots_within_reach = garden_map.get_plots_within_reach(garden_map.starting_position, 64)
    print(len(plots_within_reach))


if __name__ == '__main__':
    main()
