import sys


DIRECTIONS = {
    'R': (1, 0),
    'D': (0, 1),
    'L': (-1, 0),
    'U': (0, -1)
}


def ray_cast(row: int, lagoon_map: list[str]):
    # outside == even, inside == odd
    width = len(lagoon_map[0])
    num_intersections = [0 for _ in range(width)]
    intersection_count = 0

    for x in range(1, width):
        if lagoon_map[row][x-1:x+1] == '#.':
            intersection_count += 1
        num_intersections[x] = intersection_count

    return num_intersections


def get_lagoon_map(trench):
    width = max(x for x, _ in trench) + 1
    height = max(y for _, y in trench) + 1
    lagoon_map = []
    for y in range(height):
        lagoon_map.append(''.join('#' if (x, y) in trench else '.'
                                  for x in range(width)))
    return lagoon_map


def dig_from_point(starting_point: tuple[int], trench: set[tuple[int]]):
    lagoon = set()
    point_queue = [starting_point]

    while point_queue:
        point = point_queue.pop()
        if point not in lagoon:
            lagoon.add(point)
            x, y = point

            for dx, dy in DIRECTIONS.values():
                neighbor_point = (x+dx, y+dy)
                if neighbor_point not in trench and neighbor_point not in lagoon:
                    point_queue.append(neighbor_point)

    return lagoon | trench


def get_offset_trench(trench):
    width_offset = abs(min(x for x, _ in trench))
    height_offset = abs(min(y for _, y in trench))
    return {(x+width_offset, y+height_offset) for x, y in trench}


def dig_lagoon(trench):
    trench = get_offset_trench(trench)
    lagoon_map = get_lagoon_map(trench)
    height = len(lagoon_map)
    width = len(lagoon_map[0])
    num_intersections = [ray_cast(row, lagoon_map) for row in range(height)]
    point_inside = next((x, y) for x in range(width)
                        for y in range(height) if num_intersections[y][x] % 2 == 1 and (x, y) not in trench)
    return dig_from_point(point_inside, trench)


def main():
    filename = sys.argv[1]
    position = (0, 0)
    trench = {position}
    edge_colors = {}

    with open(filename) as dig_plan_file:
        for line in dig_plan_file:
            x, y = position
            direction, num_meters, color = line.split()
            dx, dy = DIRECTIONS[direction]

            for _ in range(int(num_meters)):
                x += dx
                y += dy
                trench.add((x, y))
                edge_colors[(x, y)] = color

            position = (x, y)

    lagoon = dig_lagoon(trench)
    print(len(lagoon))


if __name__ == '__main__':
    main()
