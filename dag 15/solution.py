def get_sensor_position(sensor_part):
    x_part, y_part = sensor_part.split()[2:]
    return int(x_part.split('=')[1][:-1]), int(y_part.split('=')[1])


def get_beacon_position(beacon_part):
    x_part, y_part = beacon_part.split()[4:]
    return int(x_part.split('=')[1][:-1]), int(y_part.split('=')[1])


def part1():
    with open('dag 15/example_input.txt') as sensor_reports:
        for sensor_report in sensor_reports:
            sensor_part, beacon_part = sensor_report.split(':')
            sensor_position = get_sensor_position(sensor_part)
            beacon_position = get_beacon_position(beacon_part)
            a = 3


if __name__ == '__main__':
    part1()
