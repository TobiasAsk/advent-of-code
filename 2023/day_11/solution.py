import sys
from itertools import combinations


def get_empty_spaces(universe_image):
    height, width = len(universe_image), len(universe_image[0])
    galaxy_free_columns = [x for x in range(width) if
                           all(universe_image[y][x] == '.' for y in range(height))]
    galaxy_free_rows = [y for y in range(height) if
                        all(universe_image[y][x] == '.' for x in range(width))]
    return galaxy_free_rows, galaxy_free_columns


def manhattan_distance(pos, other_pos):
    pos_x, pos_y = pos
    other_x, other_y = other_pos
    return abs(pos_x-other_x) + abs(pos_y-other_y)


def distance_after_expansion(
        galaxy_pos: tuple[int],
        other_galaxy_pos: tuple[int],
        empty_columns: list[int],
        empty_rows: list[int],
        scaling_factor: int) -> int:

    galaxy_x, galaxy_y = galaxy_pos
    other_galaxy_x, other_galaxy_y = other_galaxy_pos
    num_horizontal_expansions = len([x for x in empty_columns if
                                     min(galaxy_x, other_galaxy_x) < x < max(other_galaxy_x, galaxy_x)])
    num_vertical_expansions = len([y for y in empty_rows if
                                   min(galaxy_y, other_galaxy_y) < y < max(other_galaxy_y, galaxy_y)])
    distance_before = manhattan_distance(galaxy_pos, other_galaxy_pos)
    return distance_before + (scaling_factor-1) * (num_horizontal_expansions + num_vertical_expansions)


def main():
    filename = sys.argv[1]
    with open(filename) as universe_image_file:
        universe_image = universe_image_file.read().splitlines()

    height, width = len(universe_image), len(universe_image[0])
    galaxy_coordinates = [(x, y) for y in range(height) for x in range(width) if universe_image[y][x] == '#']
    empty_rows, empty_cols = get_empty_spaces(universe_image)

    distance_sum = 0
    for galaxy_pos, other_galaxy_pos in combinations(galaxy_coordinates, 2):
        distance_sum += distance_after_expansion(
            galaxy_pos,
            other_galaxy_pos,
            empty_cols,
            empty_rows,
            1000000)

    print(distance_sum)


if __name__ == '__main__':
    main()
