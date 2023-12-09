import sys


def get_differences(values: list[int]) -> list[int]:
    return [values[i] - values[i-1] for i in range(1, len(values))]


def extrapolate_value(values: list[int]) -> int:
    differences = get_differences(values)
    difference_sequences = [differences]
    while not all(v == 0 for v in differences):
        differences = get_differences(differences)
        difference_sequences.append(differences)

    all_values = list(reversed(difference_sequences)) + [values]
    for i in range(1, len(all_values)):
        placeholder_value = all_values[i][0] - all_values[i-1][0]
        all_values[i].insert(0, placeholder_value)

    return placeholder_value


def main():
    filename = sys.argv[1]
    extrapolated_values_sum = 0

    with open(filename) as oasis_report_file:
        for line in oasis_report_file:
            values = [int(v) for v in line.split()]
            extrapolated_values_sum += extrapolate_value(values)

    print(extrapolated_values_sum)


if __name__ == '__main__':
    main()
