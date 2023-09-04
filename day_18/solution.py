import sys


def get_adjacent_points(point):
    for axis in range(3):
        for direction in [-1, 1]:
            yield tuple(
                point[i] + direction if i == axis else point[i] for i in range(3))


def main():
    filename = sys.argv[1]
    num_exposed_sides = {}
    potential_pockets = {}

    with open(filename) as point_file:
        for point_line in point_file:
            point = tuple(int(c) for c in point_line.split(','))
            num_exposed_sides[point] = 6

            for other_point in get_adjacent_points(point):
                if other_point in num_exposed_sides:
                    num_exposed_sides[point] -= 1
                    num_exposed_sides[other_point] -= 1

                else:
                    potential_pockets[other_point] = (
                        1 if other_point not in potential_pockets else potential_pockets[other_point] + 1)

    pockets = [p for (p, c) in potential_pockets.items() if c == 6]

    for pocket in pockets:
        for point in get_adjacent_points(pocket):
            if num_exposed_sides[point] > 0:
                num_exposed_sides[point] -= 1

    total_surface_area = sum(n for n in num_exposed_sides.values())
    print(f'Total surface area is {total_surface_area}')


if __name__ == '__main__':
    main()
