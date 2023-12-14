import sys


def get_contigous_group_sizes(springs: str) -> list[int]:
    group_sizes = []
    group_start_idx = None
    for i in range(len(springs)):
        if springs[i] == '#':
            if group_start_idx is None:
                group_start_idx = i
        else:
            if group_start_idx is not None:
                group_sizes.append(i-group_start_idx)
                group_start_idx = None

    if group_start_idx is not None:
        group_sizes.append(i-group_start_idx+1)

    return group_sizes


def is_possible_arrangement(
        spring_row: str,
        target_group_sizes: list[int]) -> bool:

    return get_contigous_group_sizes(spring_row) == target_group_sizes


def get_replacements(spring_row: str, idx: int = 0, replacements: list[str] = []):
    if spring_row[idx:].find('?') == -1:
        replacements.append(spring_row)
        return

    damaged = spring_row[:idx] + spring_row[idx:].replace('?', '#', 1)
    operational = spring_row[:idx] + spring_row[idx:].replace('?', '.', 1)
    get_replacements(damaged, idx+1, replacements)
    get_replacements(operational, idx+1, replacements)


def get_possible_arrangements(spring_row: str) -> int:
    parts = spring_row.split()
    springs = parts[0]
    target_group_sizes = [int(s) for s in parts[1].split(',')]
    replacements = []
    get_replacements(springs, replacements=replacements)
    num_arrangements = 0
    for replacement in replacements:
        group_sizes = get_contigous_group_sizes(replacement)
        if group_sizes == target_group_sizes:
            num_arrangements += 1
    return num_arrangements


def main():
    filename = sys.argv[1]
    arrangement_count_sum = 0

    with open(filename) as spring_conditions_file:
        for spring_row in spring_conditions_file:
            arrangement_count_sum += get_possible_arrangements(spring_row)

    print(arrangement_count_sum)


if __name__ == '__main__':
    main()
