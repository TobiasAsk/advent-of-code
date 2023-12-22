import sys
from functools import cache


def parse_row(spring_row: str, unfold: bool = False) -> tuple[str, tuple[int]]:
    springs_part, sizes_part = spring_row.split()
    if unfold:
        springs_part = '?'.join(springs_part for _ in range(5))
        sizes_part = ','.join(sizes_part for _ in range(5))
    return springs_part, tuple(int(s) for s in sizes_part.split(','))


@cache
def get_num_arrangements(
        spring_conditions: str,
        group_sizes: tuple[int]) -> int:

    if not group_sizes:
        return 0 if '#' in spring_conditions else 1
    if not spring_conditions:
        return 1 if not group_sizes else 0

    total_num = 0
    if spring_conditions[0] in '.?':
        total_num += get_num_arrangements(spring_conditions[1:], group_sizes)

    if spring_conditions[0] in '#?':
        target = group_sizes[0]
        if (target <= len(spring_conditions)
            and '.' not in spring_conditions[:target]
                and (target == len(spring_conditions) or spring_conditions[target] != '#')):
            total_num += get_num_arrangements(spring_conditions[target+1:], group_sizes[1:])

    return total_num


def main():
    filename = sys.argv[1]
    arrangement_count_sum = 0

    with open(filename) as spring_conditions_file:
        for spring_row in spring_conditions_file:
            spring_conditions, target_group_sizes = parse_row(spring_row, unfold=True)
            arrangement_count_sum += get_num_arrangements(spring_conditions, target_group_sizes)

    print(arrangement_count_sum)


if __name__ == '__main__':
    main()
