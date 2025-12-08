'''Does not require search! Greedy approach from left to right works fine since order matters.'''

import sys


def get_max_and_idx(digits: list[int]) -> tuple[int, int]:
    max_digit, max_digit_idx = 0, 0
    for i, digit in enumerate(digits):
        if digit > max_digit:
            max_digit = digit
            max_digit_idx = i
    return max_digit, max_digit_idx


def find_largest_joltage(bank: list[int]) -> int:
    digits = ''
    offset = 0
    for i in range(11, -1, -1):
        bank_in_range = bank[offset:-i] if i > 0 else bank[offset:]
        max_digit_in_range, max_digit_idx = get_max_and_idx(bank_in_range)
        digits += str(max_digit_in_range)
        offset += max_digit_idx+1
    return int(digits)


def main():
    filename = sys.argv[1]
    with open(filename) as banks_file:
        banks = banks_file.read().splitlines()
        banks = [list(int(d) for d in b) for b in banks]

    joltage_sum = 0
    for bank in banks:
        joltage_sum += find_largest_joltage(bank)
    print(joltage_sum)


if __name__ == '__main__':
    main()
