import sys
from collections import namedtuple

Line = namedtuple('Line', ['is_horizontal', 'start_coordinate'])


def get_patterns(patterns_file_content: str):
    patterns = patterns_file_content.split('\n\n')
    return [p.splitlines() for p in patterns]


def find_horizontal(pattern: list[str]):
    # either the top or the bottom row must occur at least twice
    if pattern[0] in pattern[1:]:
        # line is in top half
        reflection_starts = [i for i in range(1, len(pattern)) if pattern[i] == pattern[0]]
        for reflection_start in reflection_starts:
            sub_pattern = pattern[:reflection_start+1]
            if all(sub_pattern[i] == sub_pattern[-i-1] for i in range(len(sub_pattern))):
                return len(sub_pattern) // 2

    if pattern[-1] in pattern[:-1]:
        # line is in bottom half
        reflection_starts = [i for i in range(len(pattern)-1) if pattern[i] == pattern[-1]]
        for reflection_start in reflection_starts:
            sub_pattern = pattern[reflection_start:]
            if all(sub_pattern[i] == sub_pattern[-i-1] for i in range(len(sub_pattern))):
                return reflection_start + len(sub_pattern) // 2

    return None


def find_vertical(pattern: list[str]) -> Line:
    width = len(pattern[0])
    columns = [''.join(p[i] for p in pattern) for i in range(width)]
    return find_horizontal(columns)


def find_reflection_line(pattern: list[str]) -> Line:
    horizontal = find_horizontal(pattern)
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
            f = 2
    print(col_count + row_count)


if __name__ == '__main__':
    main()
