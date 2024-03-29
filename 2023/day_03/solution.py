import sys
from collections import defaultdict

DIRECTIONS = [
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1)
]


def find_numbers(schematic_row: str):
    numbers = []
    i = 0
    while i < len(schematic_row):
        if schematic_row[i].isdigit():
            j = i
            while j < len(schematic_row) and schematic_row[j].isdigit():
                j += 1
            range_and_number = (i, j-1), int(schematic_row[i:j])
            numbers.append(range_and_number)
            i = j+1
        else:
            i += 1
    return numbers


def get_adjacent_star(
        row_number: int,
        number_range: tuple[int],
        engine_schematic: list[str]) -> bool:

    height, width = len(engine_schematic), len(engine_schematic[0])

    for x in number_range:
        for dx, dy in DIRECTIONS:
            new_x, new_y = x+dx, row_number+dy
            if (0 <= new_x < width and 0 <= new_y < height and
                    engine_schematic[new_y][new_x] == '*'):
                return new_x, new_y
    return None


def main():
    filename = sys.argv[1]
    with open(filename) as engine_schematic_file:
        engine_schematic = engine_schematic_file.read().splitlines()

    stars_to_nums = defaultdict(list)

    for row_num in range(len(engine_schematic)):
        number_ranges = find_numbers(engine_schematic[row_num])
        for number_range, number in number_ranges:
            if (star_pos := get_adjacent_star(
                    row_num, number_range, engine_schematic)) != None:
                stars_to_nums[star_pos].append(number)

    gear_ratio_sum = 0
    for adjacent_numbers in stars_to_nums.values():
        if len(adjacent_numbers) == 2:
            gear_ratio_sum += adjacent_numbers[0] * adjacent_numbers[1]

    print(gear_ratio_sum)


if __name__ == '__main__':
    main()
