import sys


def is_in_range(range: tuple[int, ...], num: int) -> bool:
    return range[0] <= num <= range[1]


def main():
    filename = sys.argv[1]
    with open(filename) as ingredient_inventory_file:
        ingredient_ranges_raw, available_ingredients = [s.splitlines()
                                                        for s in ingredient_inventory_file.read().split('\n\n')]
        ingredient_ranges = [tuple(int(d) for d in r.split('-')) for r in ingredient_ranges_raw]
        available_ingredients = [int(i) for i in available_ingredients]

    num_fresh = 0
    for ingredient in available_ingredients:
        if any(is_in_range(r, ingredient) for r in ingredient_ranges):
            num_fresh += 1
    print(num_fresh)


if __name__ == '__main__':
    main()
