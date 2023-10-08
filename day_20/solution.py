import sys


def move(elem_idx: int, num_moves: int, elements: list):
    new_idx = (elem_idx + num_moves) % (len(elements)-1)
    
    if num_moves < 0 and new_idx == 0:
        new_idx = len(elements)
    elif num_moves > 0 and new_idx == len(elements)-1:
        new_idx = 0
    
    elem = elements.pop(elem_idx)
    elements.insert(new_idx, elem)


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
