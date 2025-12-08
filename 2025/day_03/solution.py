import sys


def get_max_and_idx(digits: list[int]) -> tuple[int, int]:
    max_digit, max_digit_idx = 0, 0
    for i, digit in enumerate(digits):
        if digit > max_digit:
            max_digit = digit
            max_digit_idx = i
    return max_digit, max_digit_idx


def find_largest_joltage(bank: list[int]) -> int:
    max_first_digit, max_first_digit_idx = get_max_and_idx(bank[:-1])
    max_second_digit, _ = get_max_and_idx(bank[max_first_digit_idx+1:])
    return int(str(max_first_digit)+str(max_second_digit))


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
