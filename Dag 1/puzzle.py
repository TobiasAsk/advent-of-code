def get_total_calories(inventories: list[str]) -> dict[int, int]:
    elf = 0
    total_calories = {}
    total = 0

    for inventory_entry in inventories:
        if inventory_entry == '\n':
            total_calories[elf] = total
            total = 0
            elf += 1
        else:
            total += int(inventory_entry)

    return total_calories


def get_max(total_calories: dict[int, int]) -> int:
    max_calory_elf = max(total_calories, key=total_calories.get)
    return total_calories[max_calory_elf]


def get_top_n(total_calories: dict[int, int], n: int) -> list[tuple[int, int]]:
    elf_calorie_count_pairs = total_calories.items()
    sorted_pairs = sorted(elf_calorie_count_pairs,
                          key=lambda e: e[1], reverse=True)
    return sorted_pairs[:n]


def main():
    with open('input.txt') as inventories_file:
        total_calories = get_total_calories(inventories_file.readlines())

    max_calories = get_max(total_calories)
    print(f'Max num calories is {max_calories}')

    top_3_calories = get_top_n(total_calories, 3)
    sum_top = sum([p[1] for p in top_3_calories])
    print(f'Sum top 3 is {sum_top}')


if __name__ == '__main__':
    main()
