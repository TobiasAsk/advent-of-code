import sys


def is_mas_either_direction(letters: str) -> bool:
    return letters == 'MAS' or letters == 'SAM'


def has_cross_mas(box: list[str]) -> bool:
    diag_1 = ''.join(box[i][i] for i in range(3))
    diag_2 = ''.join(box[2-i][i] for i in range(3))
    return is_mas_either_direction(diag_1) and is_mas_either_direction(diag_2)


def main():
    filename = sys.argv[1]
    with open(filename) as something_file:
        word_search = something_file.read().splitlines()

    height = len(word_search)
    width = len(word_search[0])
    xmas_count = 0

    for y in range(1, height-1):
        for x in range(1, width-1):
            box = [word_search[y+i][x-1:x+2] for i in range(-1, 2)]
            xmas_count += has_cross_mas(box)

    print(xmas_count)


if __name__ == '__main__':
    main()
