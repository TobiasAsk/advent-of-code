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


def main():
    filename = sys.argv[1]
    with open(filename) as racetrack_file:
        racetrack_map = racetrack_file.read().splitlines()

    start_pos = get_object_position(racetrack_map, 'S')
    end_pos = get_object_position(racetrack_map, 'E')
    distances_from_end = get_distances_from_end(start_pos, end_pos, racetrack_map)

    width, height = len(racetrack_map[0]), len(racetrack_map)
    num_good_cheats = 0
    for x, y in distances_from_end.keys():
        for dx, dy in DIRECTIONS:
            if 0 <= x+2*dx < width and 0 <= y+2*dy < height:
                crosses_wall = (racetrack_map[y+dy][x+dx] == '#' and
                                racetrack_map[y+2*dy][x+2*dx] in '.E')
                if crosses_wall:
                    diff = distances_from_end[(x, y)] - distances_from_end[(x+2*dx, y+2*dy)] - 2
                    if diff >= 100:
                        num_good_cheats += 1

    print(num_good_cheats)


if __name__ == '__main__':
    main()
