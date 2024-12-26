import sys

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def get_positions(top_map, char):
    height, width = len(top_map), len(top_map[0])
    return [(x, y) for x in range(width) for y in range(height)
            if top_map[y][x] == char]


def get_peaks(top_map):
    return get_positions(top_map, 9)


def get_trailheads(top_map):
    return get_positions(top_map, 0)


def can_reach(top_map: list[str], peak_position: tuple[int], current_position: tuple[int]) -> bool:
    if peak_position == current_position:
        return True

    height, width = len(top_map), len(top_map[0])
    curr_x, curr_y = current_position
    for dx, dy in DIRECTIONS:
        new_x, new_y = curr_x+dx, curr_y+dy
        if (0 <= new_x < width and 0 <= new_y < height and
                top_map[new_y][new_x] - top_map[curr_y][curr_x] == 1):

            if can_reach(top_map, peak_position, (new_x, new_y)):
                return True

    return False


def main():
    filename = sys.argv[1]
    top_map = []
    with open(filename) as map_file:
        for row in map_file:
            top_map.append(list(map(int, row.strip())))

    trailheads = get_trailheads(top_map)
    peaks = get_peaks(top_map)
    trailhead_score_sum = 0

    for trailhead in trailheads:
        for peak in peaks:
            if can_reach(top_map, peak, trailhead):
                trailhead_score_sum += 1

    print(trailhead_score_sum)


if __name__ == '__main__':
    main()
