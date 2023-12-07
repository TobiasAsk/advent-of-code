import sys


def main():
    filename = sys.argv[1]
    with open(filename) as record_file:
        time_digits = record_file.readline().split(':')[1].split()
        race_time = int(''.join(time_digits))
        record_digits = record_file.readline().split(':')[1].split()
        record = int(''.join(record_digits))

    for charge_time in range(race_time):
        distance = charge_time * (race_time-charge_time)
        if distance > record:
            start_point = charge_time
            break

    for charge_time in range(race_time, 0, -1):
        distance = charge_time * (race_time-charge_time)
        if distance > record:
            end_point = charge_time
            break

    print(end_point-start_point+1)


if __name__ == '__main__':
    main()
