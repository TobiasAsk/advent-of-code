import sys
from functools import cache


@cache
def can_make_design(design: str, towel_patterns: set[str]) -> bool:
    if not design:
        return True

    for pattern in towel_patterns:
        if (design.startswith(pattern) and
                can_make_design(design[len(pattern):], towel_patterns)):
            return True

    return False


def main():
    filename = sys.argv[1]
    with open(filename) as input_file:
        towel_patterns_raw, designs_raw = input_file.read().split('\n\n')
        towel_patterns = frozenset(p.strip() for p in towel_patterns_raw.split(','))
        designs = designs_raw.splitlines()

    num_possible_designs = 0
    for design in designs:
        if can_make_design(design, towel_patterns):
            num_possible_designs += 1
    print(num_possible_designs)


if __name__ == '__main__':
    main()
