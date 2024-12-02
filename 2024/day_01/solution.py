import sys
from collections import defaultdict


def main():
    filename = sys.argv[1]
    counts = defaultdict(int)
    location_ids = []
    with open(filename) as location_ids_file:
        location_ids = location_ids_file.readlines()

    for line in location_ids:
        _, right = map(int, line.split())
        counts[right] += 1

    score = 0
    for line in location_ids:
        left, _ = map(int, line.split())
        score += left * counts[left]

    print(score)


if __name__ == '__main__':
    main()
