def contains(assignment: str, other_assignment: str) -> bool:
    first_start, first_end = map(int, assignment.split('-'))
    other_start, other_end = map(int, other_assignment.split('-'))
    return first_start <= other_start and first_end >= other_end


def overlaps(assignment: str, other_assignment: str) -> bool:
    first_start, first_end = map(int, assignment.split('-'))
    other_start, other_end = map(int, other_assignment.split('-'))
    starts_in_other = other_start <= first_start <= other_end
    ends_in_other = other_start <= first_end <= other_end
    starts_in_first = first_start <= other_start <= first_end
    ends_in_first = first_start <= other_end <= first_end
    return starts_in_other or ends_in_other or starts_in_first or ends_in_first


def part1():
    num_full_containments = 0
    with open('dag 4/input.txt') as assignments:
        for assignment in assignments:
            first_assignment, second_assignment = assignment.split(',')
            if (contains(first_assignment, second_assignment) or
                    contains(second_assignment, first_assignment)):
                num_full_containments += 1
    print(f'# full containments is {num_full_containments}')


def part2():
    num_overlaps = 0
    with open('dag 4/input.txt') as assignments:
        for assignment in assignments:
            first_assignment, second_assignment = assignment.split(',')
            num_overlaps += overlaps(first_assignment, second_assignment)
    print(f'# overlaps is {num_overlaps}')


if __name__ == '__main__':
    part2()
