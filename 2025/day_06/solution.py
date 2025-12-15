'''Parse column by column without splitting since whitespace is significant. Compute a problem when a column of
spaces is encountered, and once at the end for the final column.
'''

import sys
from functools import reduce
from operator import add, mul


def main():
    filename = sys.argv[1]
    with open(filename) as worksheet_file:
        worksheet = worksheet_file.read().splitlines()

    problem_operands = []
    num_rows = len(worksheet)
    operator = None
    total = 0
    for col in range(len(worksheet[0])):
        col_has_digit = False
        operand = ''
        for row in range(num_rows):
            entry = worksheet[row][col]
            if entry.isdigit():
                col_has_digit = True
                operand += entry
            elif entry in ['*', '+']:
                operator = entry

        if col_has_digit:
            problem_operands.append(int(operand))
        else:
            op = add if operator == '+' else mul
            total += reduce(op, problem_operands)
            problem_operands = []

    op = add if operator == '+' else mul
    total += reduce(op, problem_operands)

    print(total)


if __name__ == '__main__':
    main()
