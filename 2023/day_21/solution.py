import sys
from functools import cache
from collections import defaultdict, deque

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

    def get_num_plots_within_reach(
            self, position: tuple[int],
            num_steps: int) -> int:

        queue = deque([position])
        distance = {position: 0}
        steps = 0
        seen_at = defaultdict(set)
        num_plots_from = [0] * (num_steps+2)

        while steps < num_steps:
            x, y = queue.popleft()
            steps = distance[(x, y)]

            for dx, dy in DIRECTIONS:
                new_x, new_y = x+dx, y+dy

                if (0 <= new_x < self.width and 0 <= new_y < self.height and
                        self.map_lines[new_y][new_x] in ['.', 'S'] and (new_x, new_y) not in seen_at[steps]):

                    queue.append((new_x, new_y))
                    distance[(new_x, new_y)] = steps + 1
                    num_plots_from[steps+1] += 1
                    seen_at[steps].add((new_x, new_y))

        return num_plots_from[num_steps]


def main():
    filename = sys.argv[1]
    with open(filename) as garden_map_file:
        garden_map = GardenMap(garden_map_file.read().splitlines())

    num_plots_within_reach = garden_map.get_num_plots_within_reach(garden_map.starting_position, 64)
    print(num_plots_within_reach)


if __name__ == '__main__':
    main()
