import sys


def is_in_range(range: tuple[int, ...], num: int) -> bool:
    return range[0] <= num <= range[1]


def main():
    filename = sys.argv[1]
    with open(filename) as ingredient_inventory_file:
        ingredient_ranges_raw, _ = [s.splitlines()
                                    for s in ingredient_inventory_file.read().split('\n\n')]
        ingredient_ranges = [tuple(int(d) for d in r.split('-')) for r in ingredient_ranges_raw]

    ingredient_ranges = sorted(ingredient_ranges)
    num_fresh_ids = 0
    max_num = 0
    for start, end in ingredient_ranges:
        if end > max_num:
            if start > max_num:
                num_fresh_ids += end-start+1
            else:
                num_fresh_ids += end-max_num
        max_num = max(max_num, end)

    print(num_fresh_ids)


if __name__ == '__main__':
    main()
