ALL_DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def get_object_position(report_part, offset_in_part):
    x_part, y_part = report_part.split()[offset_in_part:]
    return int(x_part.split('=')[1][:-1]), int(y_part.split('=')[1])


def get_positions(sensor_report_line):
    sensor_part, beacon_part = sensor_report_line.split(':')
    return get_object_position(sensor_part, 2), get_object_position(beacon_part, 4)


def get_manhattan_distance(point, other_point):
    x, y = point
    other_x, other_y = other_point
    return abs(x - other_x) + abs(y - other_y)


def get_covered_points(sensor_position, radius, row):
    points = set()
    queue = [sensor_position]
    visited = set()
    while queue:
        point = queue.pop()
        x, y = point
        visited.add(point)
        if y == row:
            points.add(point)
            
        directions = ALL_DIRECTIONS if y != row else [(1, 0), (-1, 0)]

        for direction in directions:
            delta_x, delta_y = direction
            new_point = x + delta_x, y + delta_y
            if (get_manhattan_distance(sensor_position, new_point) <= radius and
                    new_point not in visited):
                queue.append(new_point)

    return points


def part1():
    coverage = set()
    beacon_positions = set()
    sensor_positions = []
    radii = []

    with open('dag 15/input.txt') as sensor_reports:
        for sensor_report in sensor_reports:
            sensor_position, beacon_position = get_positions(sensor_report)
            beacon_positions.add(beacon_position)
            radius = get_manhattan_distance(sensor_position, beacon_position)
            # covered_points = get_covered_points(sensor_position, radius, 2000000)
            # coverage.update(covered_points)

    # coverage.difference_update(beacon_positions)
    # print(len(coverage))


if __name__ == '__main__':
    part1()
