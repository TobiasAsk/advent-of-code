'''A variation of Dijkstra's algorithm where the queue is not filled with all the nodes initially, since
the search nodes are (pos, heading) tuples which must be discovered during traversal. Also, for part 2,
we need to find all the best paths instead of a single one, which requires some extra care when building the paths.'''

import sys
import heapq
import math
from collections import defaultdict

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def get_position(maze_map: list[str], tile: str) -> tuple[int]:
    height, width = len(maze_map), len(maze_map[0])
    return [(x, y) for x in range(width) for y in range(height)
            if maze_map[y][x] == tile][0]


def get_next_positions(maze_map, pos, heading):
    positions = []
    x, y = pos
    dx, dy = DIRECTIONS[heading]

    # go straight
    if maze_map[y+dy][x+dx] in '.E':
        next_pos = (x+dx, y+dy)
        positions.append((next_pos, heading, 1))

    # rotate
    for rot in [-1, 1]:
        positions.append((pos, (heading+rot) % 4, 1000))

    return positions


def visit_rec(
        pos_and_heading: tuple[tuple[int], int],
        previous: dict,
        tiles: set = set()):

    if pos_and_heading not in previous:
        return tiles

    all_tiles = set()
    tiles.add(pos_and_heading[0])
    for other_ph in previous[pos_and_heading]:
        all_tiles |= visit_rec(other_ph, previous, tiles)
    return all_tiles


def get_best_path(
        maze_map: list[str],
        start_pos: tuple[int],
        end_pos: tuple[int]) -> list[tuple[int]]:

    start_node = (start_pos, 0)
    distance = {start_node: 0}
    frontier = [(0, start_node)]
    expanded = set()
    previous = defaultdict(list)

    while frontier:
        dist, (pos, heading) = heapq.heappop(frontier)

        if (pos, heading) in expanded:
            continue

        expanded.add((pos, heading))

        for next_pos, next_heading, cost in get_next_positions(maze_map, pos, heading):
            distance_to_neighbor = distance[(pos, heading)] + cost
            alternative_dist = distance.get((next_pos, next_heading), math.inf)

            if distance_to_neighbor <= alternative_dist:
                distance[(next_pos, next_heading)] = distance_to_neighbor
                previous[(next_pos, next_heading)] = ([(pos, heading)] if distance_to_neighbor < alternative_dist else
                                                      previous[(next_pos, next_heading)] + [(pos, heading)])

                heapq.heappush(frontier, (distance_to_neighbor, (next_pos, next_heading)))

    print(distance[end_pos, 3])
    return previous


def print_path(path: set[tuple[int]], maze_map: list[str]):
    height, width = len(maze_map), len(maze_map[0])
    for y in range(height):
        print(''.join('O' if (x, y) in path
                      else maze_map[y][x] for x in range(width)))


def main():
    filename = sys.argv[1]
    with open(filename) as maze_map_file:
        maze_map = maze_map_file.read().splitlines()

    start_pos, end_pos = get_position(maze_map, 'S'), get_position(maze_map, 'E')
    path = get_best_path(maze_map, start_pos, end_pos)
    tiles = visit_rec((end_pos, 3), path)
    # print_path(tiles, maze_map)
    print(len(tiles))


if __name__ == '__main__':
    main()
