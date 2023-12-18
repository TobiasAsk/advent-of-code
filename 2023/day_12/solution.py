import sys


def get_groups(springs: str) -> list[tuple[int]]:
    groups = []
    group_start_idx = None
    for i in range(len(springs)):
        if springs[i] in '#?':
            if group_start_idx is None:
                group_start_idx = i
        else:
            if group_start_idx is not None:
                groups.append((group_start_idx, i))
                group_start_idx = None

    if group_start_idx is not None:
        groups.append((group_start_idx, i+1))

    return groups


def parse_row(spring_row: str, unfold: bool = False) -> tuple[str, list[int]]:
    springs_part, sizes_part = spring_row.split()
    if unfold:
        springs_part = '?'.join(springs_part for _ in range(5))
        sizes_part = ','.join(sizes_part for _ in range(5))
    return springs_part, [int(s) for s in sizes_part.split(',')]


def is_consistent_up_to(
        spring_conditions: str,
        target_group_sizes: list[int],
        idx: int) -> bool:
    '''
    is_consistent('.#.#.[...]', [1, 3, 1, 6]) -> False
    is_consistent('#??.[...]', [3]) -> True
    '''
    groups = get_groups(spring_conditions)
    if spring_conditions.count('#') > sum(target_group_sizes):
        return False
    if spring_conditions.count('?') + spring_conditions.count('#') < sum(target_group_sizes):
        return False

    for i in range(min(len(groups), len(target_group_sizes))):
        group_start, group_end = groups[i]
        if group_start >= idx:
            continue

        if group_end-group_start < target_group_sizes[i]:
            return False

        elif (spring_conditions[group_start:group_end].count('#') > target_group_sizes[i]
              and spring_conditions[group_start:group_end].count('?') == 0):
            return False

    return True


def solve(
        spring_conditions: str,
        target_group_sizes: list[int],
        possible: list[str]) -> str:

    first_unknown_idx = spring_conditions.find('?')

    if first_unknown_idx == -1:
        first_unknown_idx = len(spring_conditions)

    if not is_consistent_up_to(spring_conditions, target_group_sizes, first_unknown_idx):
        return False

    if '?' not in spring_conditions:
        return spring_conditions

    if (operational := solve(spring_conditions.replace('?', '.', 1), target_group_sizes, possible)):
        possible.append(operational)

    if (damaged := solve(spring_conditions.replace('?', '#', 1), target_group_sizes, possible)):
        possible.append(damaged)


def main():
    filename = sys.argv[1]
    arrangement_count_sum = 0

    with open(filename) as spring_conditions_file:
        for spring_row in spring_conditions_file:
            spring_conditions, target_group_sizes = parse_row(spring_row)
            possible = []
            solve(spring_conditions, target_group_sizes, possible)
            orig = len(possible)
            add_to_start = spring_conditions[-1] == '.'
            with_extra_unknown = '?' + spring_conditions if add_to_start else spring_conditions  +'?'
            possible_extra = []
            solve(with_extra_unknown, target_group_sizes, possible_extra)
            g = orig * len(possible_extra) ** 4
            arrangement_count_sum += g

    print(arrangement_count_sum)


if __name__ == '__main__':
    main()
