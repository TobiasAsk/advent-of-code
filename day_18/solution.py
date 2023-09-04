import sys

DIRECTIONS = [
    (1, 0),  # right
    (-1, 0),  # left
    (0, -1),  # up
    (0, 1)   # down
]

MAX_DEPTH = 10


def get_adjacent_points(point):
    num_dims = len(point)
    for axis in range(num_dims):
        for direction in [-1, 1]:
            yield tuple(
                point[i] + direction if i == axis else point[i] for i in range(num_dims))


def get_pockets(point, cubes, visited=set(), depth=0):
    if depth == MAX_DEPTH:
        return None

    pockets = [point]
    x, y = point

    for direction in DIRECTIONS:
        delta_x, delta_y = direction
        new_position = (x+delta_x, y+delta_y)
        if new_position not in cubes and new_position not in visited:
            res = get_pockets(new_position, cubes, visited | {point}, depth+1)
            if res:
                pockets.extend(res)
            else:
                return None

    return pockets


def main():
    filename = sys.argv[1]
    num_exposed_sides = {}
    potential_pockets = {}

    with open(filename) as point_file:
        for point_line in point_file:
            point = tuple(int(c) for c in point_line.split(','))
            num_exposed_sides[point] = 2*len(point)

            for other_point in get_adjacent_points(point):
                if other_point in num_exposed_sides:
                    num_exposed_sides[point] -= 1
                    num_exposed_sides[other_point] -= 1

                else:
                    potential_pockets[other_point] = (
                        1 if other_point not in potential_pockets else potential_pockets[other_point] + 1)

    all_pockets = []
    for pot_pocket in potential_pockets:
        if pot_pocket not in all_pockets:
            pockets = get_pockets(pot_pocket, num_exposed_sides.keys())
            if pockets:
                all_pockets.extend(pockets)

    for pocket in all_pockets:
        for point in get_adjacent_points(pocket):
            if point in num_exposed_sides and num_exposed_sides[point] > 0:
                num_exposed_sides[point] -= 1

    total_surface_area = sum(n for n in num_exposed_sides.values())
    print(f'Total surface area is {total_surface_area}')


if __name__ == '__main__':
    main()
