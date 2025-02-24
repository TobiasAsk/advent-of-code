import sys
import heapq
import math

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


def get_lowest_score(maze_map: list[str], start_pos: tuple[int], end_pos: tuple[int]) -> int:
    distance = {(start_pos, 0): 0}
    frontier = [(0, (start_pos, 0))]
    expanded = set()

    while frontier:
        dist_to_pos, (pos, heading) = heapq.heappop(frontier)
        if pos == end_pos:
            return dist_to_pos
        expanded.add((pos, heading))

        for next_pos, heading, cost in get_next_positions(maze_map, pos, heading):
            distance_to_neighbor = dist_to_pos + cost
            if distance_to_neighbor < distance.get((next_pos, heading), math.inf):
                distance[(next_pos, heading)] = distance_to_neighbor

            if ((next_pos, heading) not in expanded and
                    (distance_to_neighbor, (next_pos, heading)) not in frontier):
                heapq.heappush(frontier, (distance_to_neighbor, (next_pos, heading)))

    raise Exception


def main():
    filename = sys.argv[1]
    with open(filename) as maze_map_file:
        maze_map = maze_map_file.read().splitlines()

    start_pos, end_pos = get_position(maze_map, 'S'), get_position(maze_map, 'E')
    score = get_lowest_score(maze_map, start_pos, end_pos)
    print(score)


if __name__ == '__main__':
    main()
