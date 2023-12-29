import sys
from collections import namedtuple

Line = namedtuple('Line', ['is_horizontal', 'start_coordinate'])


def binary(pattern: list[str]):
    return [int(p.replace('#', '1').replace('.', '0'), 2) for p in pattern]


def get_patterns(patterns_file_content: str):
    patterns = patterns_file_content.split('\n\n')
    return [p.splitlines() for p in patterns]


def is_smudge(pattern, other_pattern):
    xored = pattern ^ other_pattern
    return xored != 0 and xored & (xored - 1) == 0


def get_xor_sum(numbers: list[int]) -> int:
    xor_sum = 0
    for num in numbers:
        xor_sum ^= num
    return xor_sum


def find_horizontal(pattern: list[int]):
    # either the top or the bottom row must either occur at least once elsewhere, or be a smudge pair
    # with a row

    # top half
    for i in range(1, len(pattern)):
        if pattern[0] == pattern[i] or is_smudge(pattern[0], pattern[i]):
            sub_pattern = pattern[:i+1]
            if len(sub_pattern) % 2 == 0:
                mid = len(sub_pattern) // 2
                top_half_xor_sum = get_xor_sum(sub_pattern[:mid])
                bottom_half_xor_sum = get_xor_sum(sub_pattern[mid:])

                if is_smudge(top_half_xor_sum, bottom_half_xor_sum):
                    return mid

    # bottom half
    for i in range(len(pattern)-2, -1, -1):
        if pattern[-1] == pattern[i] or is_smudge(pattern[-1], pattern[i]):
            sub_pattern = pattern[i:]
            if len(sub_pattern) % 2 == 0:
                mid = len(sub_pattern) // 2
                top_half_xor_sum = get_xor_sum(sub_pattern[:mid])
                bottom_half_xor_sum = get_xor_sum(sub_pattern[mid:])

                if is_smudge(top_half_xor_sum, bottom_half_xor_sum):
                    return i + mid

    return None


def find_vertical(pattern: list[str]) -> Line:
    width = len(pattern[0])
    columns = [''.join(p[i] for p in pattern) for i in range(width)]
    return find_horizontal(binary(columns))


def find_reflection_line(pattern: list[str]) -> Line:
    horizontal = find_horizontal(binary(pattern))
    if horizontal:
        return Line(True, horizontal)
    return Line(False, find_vertical(pattern))


def main():
    filename = sys.argv[1]
    with open(filename) as patterns_file:
        patterns = get_patterns(patterns_file.read())

    col_count, row_count = 0, 0
    for i, pattern in enumerate(patterns):
        line = find_reflection_line(pattern)
        if line.start_coordinate:
            if line.is_horizontal:
                row_count += 100 * line.start_coordinate
            else:
                col_count += line.start_coordinate
        else:
            assert False, f"Couldn't find reflection line in pattern {i+1}"

    print(col_count + row_count)


if __name__ == '__main__':
    main()
