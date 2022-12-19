import timeit


def get_priority(item_type: str):
    return (ord(item_type) - 96 if item_type.islower()
            else ord(item_type) - 64 + 26)


def find_error_double_loop(left_compartment, right_compartment):
    for item in left_compartment:
        for other_item in right_compartment:
            if item == other_item:
                return item


def find_error_race(left_compartment, right_compartment):
    sorted_left, sorted_right = sorted(
        left_compartment), sorted(right_compartment)
    left_idx = right_idx = 0

    while sorted_left[left_idx] != sorted_right[right_idx]:
        left_ord = ord(sorted_left[left_idx])
        right_ord = ord(sorted_right[right_idx])
        if left_ord < right_ord:
            left_idx += 1
        else:
            right_idx += 1

    return sorted_left[left_idx]


def part_1_fast_maybe(rucksacks):
    priority_sum = 0
    for rucksack in rucksacks:
        mid = len(rucksack) // 2
        left_compartment, right_compartment = rucksack[:mid], rucksack[mid:]
        error = find_error_race(left_compartment, right_compartment)
        priority_sum += get_priority(error)


def part_1_slow_maybe(rucksacks):
    priority_sum = 0
    for rucksack in rucksacks:
        mid = len(rucksack) // 2
        left_compartment, right_compartment = rucksack[:mid], rucksack[mid:]
        error = find_error_double_loop(left_compartment, right_compartment)
        priority_sum += get_priority(error)


def get_badge(group):
    first, second, third = set(group[0]), set(group[1]), set(group[2])
    return list(first.intersection(second).intersection(third))[0]


def part_2(rucksacks):
    priority_sum = 0
    for i in range(0, len(rucksacks), 3):
        group = rucksacks[i:i+3]
        badge = get_badge(group)
        priority_sum += get_priority(badge)
    print(f'Sum is {priority_sum}')


if __name__ == '__main__':
    with open('dag 3/input.txt') as rucksacks_file:
        rucksacks = list(map(str.strip, rucksacks_file.readlines()))
    slow = timeit.timeit(lambda: part_1_slow_maybe(rucksacks), number=10000)
    print(slow)
    fast = timeit.timeit(lambda: part_1_fast_maybe(rucksacks), number=10000)
    print(fast)
    # part_2(rucksacks)
