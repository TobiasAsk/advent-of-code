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
    return get_positions(top_map, '9')


def get_trailheads(top_map):
    return get_positions(top_map, '0')


def get_num_trails(top_map: list[str], peak_position: tuple[int], current_position: tuple[int]) -> int:
    if peak_position == current_position:
        return 1

    height, width = len(top_map), len(top_map[0])
    curr_x, curr_y = current_position
    num_trails = 0

    for dx, dy in DIRECTIONS:
        new_x, new_y = curr_x+dx, curr_y+dy
        if (0 <= new_x < width and 0 <= new_y < height and
                top_map[new_y][new_x] != '.' and
                int(top_map[new_y][new_x]) - int(top_map[curr_y][curr_x]) == 1):

            num_trails += get_num_trails(top_map, peak_position, (new_x, new_y))

    return num_trails


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        top_map = map_file.read().splitlines()

    trailheads = get_trailheads(top_map)
    peaks = get_peaks(top_map)
    trailhead_rating_sum = 0

    for trailhead in trailheads:
        for peak in peaks:
            trailhead_rating_sum += get_num_trails(top_map, peak, trailhead)

    print(trailhead_rating_sum)


if __name__ == '__main__':
    main()
