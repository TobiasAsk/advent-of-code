import sys
from functools import cache


@cache
def num_ways_to_make(design: str, towel_patterns: set[str]) -> int:
    if not design:
        return 1

    num_ways = 0
    for pattern in towel_patterns:
        if design.startswith(pattern):
            num_ways += num_ways_to_make(design[len(pattern):], towel_patterns)

    return num_ways


def main():
    filename = sys.argv[1]
    with open(filename) as input_file:
        towel_patterns_raw, designs_raw = input_file.read().split('\n\n')
        towel_patterns = frozenset(p.strip() for p in towel_patterns_raw.split(','))
        designs = designs_raw.splitlines()

    all_options = 0
    for design in designs:
        all_options += num_ways_to_make(design, towel_patterns)
    print(all_options)


if __name__ == '__main__':
    main()
