import sys
import re
from enum import StrEnum


class Token(StrEnum):
    MUL = 'MUL'
    DO = 'DO'
    DONT = "DONT"


TOKENS = [
    (Token.MUL, r'mul\((\d{1,3}),(\d{1,3})\)'),
    (Token.DO, r'do\(\)'),
    (Token.DONT, r"don't\(\)")
]


def main():
    filename = sys.argv[1]
    with open(filename) as instructions_file:
        instructions = instructions_file.read()

    all_tokens = '|'.join(f'(?P<{t}>{p})' for t, p in TOKENS)
    enabled = True
    mul_sum = 0
    for match in re.finditer(all_tokens, instructions):
        type = match.lastgroup
        if type == Token.MUL and enabled:
            left_op, right_op = int(match.group(2)), int(match.group(3))
            mul_sum += left_op * right_op
        elif type == Token.DO:
            enabled = True
        elif type == Token.DONT:
            enabled = False

    print(mul_sum)


if __name__ == '__main__':
    main()
