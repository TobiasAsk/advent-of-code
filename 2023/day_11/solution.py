import sys
from itertools import combinations


def expand_universe(universe_image):
    expanded = list(universe_image)
    height, width = len(universe_image), len(universe_image[0])
    galaxy_free_columns = [x for x in range(width) if
                           all(universe_image[y][x] == '.' for y in range(height))]
    galaxy_free_rows = [y for y in range(height) if
                        all(universe_image[y][x] == '.' for x in range(width))]

    for row in range(height):
        for i, column in enumerate(galaxy_free_columns):
            expanded[row] = expanded[row][:column+i] + '.' + expanded[row][column+i:]

    for i, row in enumerate(galaxy_free_rows):
        expanded.insert(row+i, '.'*(width+len(galaxy_free_columns)))

    return expanded


def manhattan_distance(pos, other_pos):
    pos_x, pos_y = pos
    other_x, other_y = other_pos
    return abs(pos_x-other_x) + abs(pos_y-other_y)


def main():
    filename = sys.argv[1]
    with open(filename) as universe_image_file:
        universe_image = universe_image_file.read().splitlines()

    expanded_universe = expand_universe(universe_image)
    height, width = len(expanded_universe), len(expanded_universe[0])
    galaxy_coordinates = [(x, y) for x in range(width) for y in range(height) if expanded_universe[y][x] == '#']

    distance_sum = 0
    for galaxy_pos, other_galaxy_pos in combinations(galaxy_coordinates, 2):
        distance_sum += manhattan_distance(galaxy_pos, other_galaxy_pos)

    print(distance_sum)


if __name__ == '__main__':
    main()
