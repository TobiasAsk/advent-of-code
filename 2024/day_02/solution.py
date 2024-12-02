import sys


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
            num_safe += is_safe(levels)

    print(num_safe)

if __name__ == '__main__':
    main()
