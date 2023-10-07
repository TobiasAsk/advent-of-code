import sys


def move(elem_idx: int, num_moves: int, elements: list):
    i = elem_idx
    for _ in range(abs(num_moves)):

        if (num_moves < 0 and i > 1) or (num_moves > 0 and i < len(elements)-2):
            next_idx = i+1 if num_moves > 0 else i-1
            elements[i], elements[next_idx] = elements[next_idx], elements[i]
            i += 1 if num_moves > 0 else -1

        else:
            elem = elements.pop(i)
            i = len(elements) if num_moves < 0 else 0
            elements.insert(i, elem)


def main():
    filename = sys.argv[1]
    with open(filename) as number_list:
        original_numbers = [int(n) for n in number_list]

    numbers = list(original_numbers)
    for number in original_numbers:
        # this makes it O(n^2). Might be OK, else some index tracking is needed
        number_idx = numbers.index(number)
        move(elem_idx=number_idx, num_moves=number, elements=numbers)

    start_idx = numbers.index(0)
    coordinate_sum = 0
    for i in range(1000, 3001, 1000):
        idx = (start_idx + i) % len(numbers)
        coordinate_sum += numbers[idx]
    print(f'Coordinate sum is {coordinate_sum}')


def test(elem: int, nums: list, expected: list):
    elem_idx = nums.index(elem)
    move(elem_idx, elem, nums)
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
    ]
    for elem, nums, expected in test_cases:
        test(elem, nums, expected)
    print('Tests pass')

    main()
