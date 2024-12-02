import sys


def is_safe_remove_one(levels: list[int]) -> bool:
    for i in range(len(levels)):
        new_levels = levels[:i] + levels[i+1:]
        if is_safe(new_levels):
            return True
    return False


def is_safe(levels: list[int]) -> bool:
    increasing = None
    for i in range(1, len(levels)):
        previous_level, level = levels[i-1], levels[i]
        diff = previous_level - level
        if increasing is None:
            increasing = diff > 0

        valid_diff = (increasing and diff > 0) or (not increasing and diff < 0)

        if abs(diff) > 3 or not valid_diff:
            return False

    return True


def main():
    filename = sys.argv[1]
    num_safe = 0
    with open(filename) as reports:
        for report in reports:
            levels = list(map(int, report.split()))
            if is_safe(levels):
                num_safe += 1
            else:
                num_safe += is_safe_remove_one(levels)

    print(num_safe)


if __name__ == '__main__':
    main()
