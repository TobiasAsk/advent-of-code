import multiprocessing
import functools

MAX_COORD = 4000000
MIN_COORD = 0


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


def get_row_coverage(row, sensor_positions, radii):
    row_coverage = [0] * (MAX_COORD + 1)
    for i in range(len(sensor_positions)):
        sensor_x, sensor_y = sensor_positions[i]
        radius = radii[i]
        diff_y = abs(sensor_y - row)

        if diff_y <= radius:
            delta_x = abs(diff_y - radius)
            start_x = max(sensor_x - delta_x, MIN_COORD)
            end_x = min(sensor_x + delta_x, MAX_COORD)
            row_coverage[start_x:end_x+1] = [1] * (end_x-start_x+1)

    return row_coverage


def part2():
    sensor_positions = []
    radii = []

    with open('dag 15/input.txt') as sensor_reports:
        for sensor_report in sensor_reports:
            sensor_position, beacon_position = get_positions(sensor_report)
            radius = get_manhattan_distance(sensor_position, beacon_position)
            sensor_positions.append(sensor_position)
            radii.append(radius)

    with multiprocessing.Pool(6) as pool:
        func = functools.partial(
            get_row_coverage, sensor_positions=sensor_positions, radii=radii)

        results = pool.imap(func, range(MAX_COORD), MAX_COORD//10)
        for r in results:
            if r.count(0) > 0:
                print('bl')


if __name__ == '__main__':
    part2()
