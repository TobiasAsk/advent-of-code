import sys


def move(number: int, numbers: list):
    number_indices = [i for i in range(len(numbers)) if numbers[i] == number]
    num_steps = number
    indices = list(reversed(number_indices)
                   ) if num_steps > 0 else list(number_indices)

    for i in range(len(indices)):
        number_idx = indices[i]
        new_idx = (number_idx + num_steps) % (len(numbers)-1)

        if num_steps < 0 and new_idx == 0:
            new_idx = len(numbers)
        elif num_steps > 0 and new_idx == len(numbers)-1:
            new_idx = 0

        popped = numbers.pop(number_idx)
        numbers.insert(new_idx, popped)

        for j in range(i+1, len(indices)):
            if indices[j] > new_idx and number_idx > indices[j]:
                indices[j] += 1
            elif indices[j] < new_idx and number_idx < indices[j]:
                indices[j] -= 1


def main():
    filename = sys.argv[1]
    with open(filename) as number_list:
        original_numbers = [int(n) for n in number_list]

    numbers = list(original_numbers)
    for number in original_numbers:
        move(number=number, numbers=numbers)

    start_idx = numbers.index(0)
    coordinate_sum = sum(numbers[(start_idx+offset) % len(numbers)]
                         for offset in [1000, 2000, 3000])
    print(f'Coordinate sum is {coordinate_sum}')


def test(number: int, nums: list, expected: list):
    move(number, nums)
    assert nums == expected, f'Expected {expected}, got {nums}'


if __name__ == '__main__':
    test_cases = [
        (-2, [1, 2, -2, -3, 0, 3, 4], [1, 2, -3, 0, 3, 4, -2]),
        (-3, [1, -3, 2, 3, -2, 0, 4], [1, 2, 3, -2, -3, 0, 4]),
        (3, [1, -3, 2, 3, -2, 0, 4], [3, 1, -3, 2, -2, 0, 4]),
        (2, [1, 1, 1, 2, 1, 1], [2, 1, 1, 1, 1, 1]),
        (2, [1, 1, 1, 2, 1, 1, 1], [1, 1, 1, 1, 1, 2, 1]),
        (-10, [1, 1, 1, -10, 1, 1], [1, 1, 1, -10, 1, 1]),
        (10, [1, 1, 1, 10, 1, 1], [1, 1, 1, 10, 1, 1]),

        # duplicates
        (5,
         [5, 1, 2, 5, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14],
         [1, 2, 3, 4, 6, 5, 7, 8, 5, 9, 10, 11, 12, 13, 14]),

        (-3,
         [1, 2, 3, 4, -3, 5, 6, -3],
         [1, -3, 2, 3, -3, 4, 5, 6]),

        (4,
         [1, 2, 4, 3, 5, 4, 6, 7, 8],
         [1, 4, 2, 3, 5, 6, 7, 4, 8]),

        (-3,
         [1, 1, -3, 1, 1, 1, 1, 1, -3, 1, 1, 1],
         [1, 1, 1, 1, -3, 1, 1, 1, 1, 1, -3, 1]),
    ]

    for elem, nums, expected in test_cases:
        test(elem, nums, expected)
    print('Tests pass')

    main()
