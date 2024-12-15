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
        for loc, other_loc in it.combinations(antenna_locations, 2):
            x, y = loc
            other_x, other_y = other_loc
            dx, dy = x-other_x, y-other_y

            first_antinode_x, first_antinode_y = x+dx, y+dy
            second_antinode_x, second_antinode_y = other_x-dx, other_y-dy

            if 0 <= first_antinode_x < width and 0 <= first_antinode_y < height:
                antinode_positions.add((first_antinode_x, first_antinode_y))

            if 0 <= second_antinode_x < width and 0 <= second_antinode_y < height:
                antinode_positions.add((second_antinode_x, second_antinode_y))

    print(len(antinode_positions))


if __name__ == '__main__':
    main()
