import sys

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


def has_adjacent_symbol(
        row_number: int,
        number_range: tuple[int],
        engine_schematic: list[str]) -> bool:

    height, width = len(engine_schematic), len(engine_schematic[0])

    for x in number_range:
        for dx, dy in DIRECTIONS:
            new_x, new_y = x+dx, row_number+dy
            if (0 <= new_x < width and 0 <= new_y < height and
                    engine_schematic[new_y][new_x] not in '0123456789.'):
                return True
    return False


def main():
    filename = sys.argv[1]
    with open(filename) as engine_schematic_file:
        engine_schematic = engine_schematic_file.read().splitlines()

    part_number_sum = 0
    for row_num in range(len(engine_schematic)):
        number_ranges = find_numbers(engine_schematic[row_num])
        for number_range, number in number_ranges:
            if has_adjacent_symbol(row_num, number_range, engine_schematic):
                part_number_sum += number

    print(part_number_sum)


if __name__ == '__main__':
    main()
