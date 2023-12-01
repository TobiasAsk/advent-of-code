import sys

DIRECTIONS_2D = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

DIRECTIONS_3D = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def get_adjacent_points_3d(point):
    x, y, z = point

    for direction in DIRECTIONS_3D:
        delta_x, delta_y, delta_z = direction
        yield (x+delta_x, y+delta_y, z+delta_z)


def within_bounds(point, bounds):
    x, y, z = point
    min_x, min_y, min_z, max_x, max_y, max_z = bounds
    return min_x <= x < max_x and min_y <= y < max_y and min_z <= z < max_z


def flood_fill_iterative(point, cubes, bounds):
    q = [point]
    visited = set()
    count = 0

    while q:
        p = q.pop()
        if p not in visited:
            visited.add(p)

            for other_point in get_adjacent_points_3d(p):
                if other_point in cubes:
                    count += 1

                elif within_bounds(other_point, bounds) and (other_point not in visited):
                    q.append(other_point)

    return count


def main():
    filename = sys.argv[1]
    cubes = set()
    min_x, min_y, min_z, max_x, max_y, max_z = 100, 100, 100, -100, -100, -100

    with open(filename) as cube_file:
        for cube_line in cube_file:
            cube = tuple(int(c) for c in cube_line.split(','))
            cubes.add(cube)
            min_x = min(min_x, cube[0])
            max_x = max(max_x, cube[0])

            min_y = min(min_y, cube[1])
            max_y = max(max_y, cube[1])

            min_z = min(min_z, cube[2])
            max_z = max(max_z, cube[2])

    start_point = (min_x-1, min_y-1, min_z-1)
    bounds = (min_x-2, min_y-2, min_z-2, max_x+2, max_y+2, max_z+2)

    num_exposed_sides = flood_fill_iterative(start_point, cubes, bounds)
    print(f'Total surface area is {num_exposed_sides}')


if __name__ == '__main__':
    main()
