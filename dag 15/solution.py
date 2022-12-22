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


def part1():
    beacon_positions = set()
    sensor_positions = []
    radii = []
    row = 2000000

    with open('dag 15/input.txt') as sensor_reports:
        for sensor_report in sensor_reports:
            sensor_position, beacon_position = get_positions(sensor_report)
            beacon_positions.add(beacon_position)
            radius = get_manhattan_distance(sensor_position, beacon_position)
            sensor_positions.append(sensor_position)
            radii.append(radius)

    covered_on_row = set()
    for i in range(len(sensor_positions)):
        sensor_x, sensor_y = sensor_positions[i]
        radius = radii[i]
        diff_y = abs(sensor_y - row)
        if diff_y <= radius:
            delta_x = abs(diff_y - radius)
            x = sensor_x - delta_x
            while x <= sensor_x + delta_x:
                point = (x, row)
                if not point in beacon_positions:
                    covered_on_row.add(point)
                x += 1

    print(len(covered_on_row))


if __name__ == '__main__':
    part1()
