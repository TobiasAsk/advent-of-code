import sys
from collections import defaultdict
import itertools as it


def get_antenna_locations(antenna_map):
    antennas = defaultdict(list)
    height, width = len(antenna_map), len(antenna_map[0])

    for y in range(height):
        for x in range(width):
            char = antenna_map[y][x]
            if char not in ('.', '#'):
                antennas[char].append((x, y))

    return antennas


def print_map(antenna_map, antinode_positions):
    height, width = len(antenna_map), len(antenna_map[0])
    for row in range(height):
        print(''.join('#' if (x, row) in antinode_positions else antenna_map[row][x]
                      for x in range(width)))


def main():
    filename = sys.argv[1]
    with open(filename) as antenna_map_file:
        antenna_map = antenna_map_file.read().splitlines()

    height, width = len(antenna_map), len(antenna_map[0])
    antennas = get_antenna_locations(antenna_map)
    antinode_positions = set()
    for antenna_locations in antennas.values():
        antinode_positions.update(antenna_locations)
        for loc, other_loc in it.combinations(antenna_locations, 2):
            x, y = loc
            other_x, other_y = other_loc
            dx, dy = x-other_x, y-other_y
            mult = 1
            first_dir_in_bounds, second_dir_in_bounds = True, True

            while first_dir_in_bounds or second_dir_in_bounds:
                first_antinode_x, first_antinode_y = x+dx*mult, y+dy*mult
                second_antinode_x, second_antinode_y = other_x-dx*mult, other_y-dy*mult

                if 0 <= first_antinode_x < width and 0 <= first_antinode_y < height:
                    antinode_positions.add((first_antinode_x, first_antinode_y))
                else:
                    first_dir_in_bounds = False

                if 0 <= second_antinode_x < width and 0 <= second_antinode_y < height:
                    antinode_positions.add((second_antinode_x, second_antinode_y))
                else:
                    second_dir_in_bounds = False

                mult += 1

    print(len(antinode_positions))
    # print_map(antenna_map, antinode_positions)


if __name__ == '__main__':
    main()
