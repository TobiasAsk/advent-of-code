''' Dynamic programming. Expand each stone, recurse the replacement until completion and cache the result.
Use tuples since lists aren't hashable, and note the horrible Python syntax for one-element tuples: (a,).
'''

import sys
import math
from functools import cache


def get_num_digits(stone_number):
    return int(math.log10(stone_number)) + 1


def get_new_stones(stone_number: int) -> tuple[int]:
    if stone_number == 0:
        return (1,)

    if get_num_digits(stone_number) % 2 == 0:
        str_num = str(stone_number)
        mid_idx = len(str_num) // 2
        return tuple(map(int, [str_num[:mid_idx], str_num[mid_idx:]]))

    return (stone_number*2024,)


@cache
def get_num_stones(stones: tuple[int], num_remaining_blinks: int) -> int:
    if num_remaining_blinks == 0:
        return len(stones)

    num_stones = 0
    for stone in stones:
        replaced = get_new_stones(stone)
        num_stones += get_num_stones(replaced, num_remaining_blinks-1)
    return num_stones


def main():
    filename = sys.argv[1]
    with open(filename) as stones_input_file:
        stones = tuple(map(int, stones_input_file.readline().split()))
    num_stones = get_num_stones(stones, 75)
    print(num_stones)
    print(get_num_stones.cache_info())


if __name__ == '__main__':
    main()
