import sys


DIRECTIONS = [
    (1, 0),
    (0, 1),
    (1, 1),
    (-1, 1)
]


def is_xmas_either_direction(letters: str) -> bool:
    return letters == 'XMAS' or letters == 'SAMX'


def main():
    filename = sys.argv[1]
    with open(filename) as something_file:
        word_search = something_file.read().splitlines()

    height = len(word_search)
    width = len(word_search[0])
    xmas_count = 0

    for y in range(height):
        for x in range(width):
            for dx, dy in DIRECTIONS:
                letters = ''.join(word_search[y+dy*i][x+dx*i] for i in range(4)
                                  if 0 <= x+dx*i < width and 0 <= y+dy*i < height)
                xmas_count += is_xmas_either_direction(letters)

    print(xmas_count)


if __name__ == '__main__':
    main()
