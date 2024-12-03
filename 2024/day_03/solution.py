import sys
import re


MUL_PATTERN = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')


def main():
    filename = sys.argv[1]
    with open(filename) as instructions_file:
        instructions = instructions_file.read()
    matches = MUL_PATTERN.findall(instructions)
    mul_sum = 0
    for left_op, right_op in [tuple(map(int, m)) for m in matches]:
        mul_sum += left_op * right_op
    print(mul_sum)


if __name__ == '__main__':
    main()
