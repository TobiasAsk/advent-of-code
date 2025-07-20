import sys

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def get_object_position(racetrack_map: list[str], object: str) -> set[tuple[int]]:
    width, height = len(racetrack_map[0]), len(racetrack_map)
    return [(x, y) for x in range(width) for y in range(height) if
            racetrack_map[y][x] == object][0]


def get_path(start_pos: tuple[int], racetrack_map: list[str]) -> list[tuple[int]]:
    queue = [start_pos]
    visited = set()
    path = []
    while queue:
        pos = queue.pop()
        visited.add(pos)
        x, y = pos
        path.append(pos)
        for dx, dy in DIRECTIONS:
            if racetrack_map[y+dy][x+dx] in '.E' and (x+dx, y+dy) not in visited:
                queue.append((x+dx, y+dy))
    return path


def get_distances_from_end(start_pos: tuple[int], end_pos: tuple[int], racetrack_map: list[str]) -> dict:
    path = get_path(start_pos, racetrack_map)
    length = len(path)-1
    return {p: length-i for i, p in enumerate(path)}


def manhattan_distance(point: tuple[int], other_point: tuple[int]) -> int:
    return abs(point[0]-other_point[0]) + abs(point[1]-other_point[1])


def get_all_reachable(pos: tuple[int], distance: int) -> set[tuple[int]]:
    x, y = pos
    return {(x+dx, y+dy) for dx in range(-distance, distance+1) for dy in range(-distance, distance+1)
            if manhattan_distance(pos, (x+dx, y+dy)) <= distance}


def main():
    filename = sys.argv[1]
    with open(filename) as racetrack_file:
        racetrack_map = racetrack_file.read().splitlines()

    start_pos = get_object_position(racetrack_map, 'S')
    end_pos = get_object_position(racetrack_map, 'E')
    distances_from_end = get_distances_from_end(start_pos, end_pos, racetrack_map)

    num_good_cheats = 0
    path = distances_from_end.keys()
    for pos in path:
        twenty_dist = get_all_reachable(pos, 20)
        tiles_within_reach = twenty_dist & path
        for other_pos in tiles_within_reach:
            dist_diff = distances_from_end[pos] - distances_from_end[other_pos]
            save = dist_diff - manhattan_distance(pos, other_pos)
            if save >= 100:
                num_good_cheats += 1

    print(num_good_cheats)


def test():
    reachable = get_all_reachable((0, 0), 3)
    assert len(reachable) == 25


if __name__ == '__main__':
    test()
    main()
