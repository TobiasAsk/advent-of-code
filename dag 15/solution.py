MAX_COORD = 1*10**4
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


def get_row_coverage(row, sensor_position, radius):
    sensor_x, sensor_y = sensor_position
    diff_y = abs(sensor_y - row)
    delta_x = abs(diff_y - radius)
    start_x = max(sensor_x - delta_x, MIN_COORD)
    end_x = min(sensor_x + delta_x, MAX_COORD)
    return start_x, end_x


def part2():
    sensor_positions = []
    radii = []

    with open('dag 15/input.txt') as sensor_reports:
        for sensor_report in sensor_reports:
            sensor_position, beacon_position = get_positions(sensor_report)
            radius = get_manhattan_distance(sensor_position, beacon_position)
            sensor_positions.append(sensor_position)
            radii.append(radius)

    total_coverage = [[0] * (MAX_COORD+1) for _ in range(MAX_COORD+1)]
    for i in range(len(sensor_positions)):
        sensor_y = sensor_positions[i][1]
        radius = radii[i]
        for direction in [1, -1]:
            for y_distance in range(radius):
                row = sensor_y + direction * y_distance
                if row < MIN_COORD or row > MAX_COORD:
                    break
                sensor_coverage_start, sensor_coverage_end = get_row_coverage(row, sensor_positions[i], radius)
                total_coverage[row][sensor_coverage_start:sensor_coverage_end+1] = [1] * (sensor_coverage_end-sensor_coverage_start+1)
    a = 2
              
if __name__ == '__main__':
    part2()
