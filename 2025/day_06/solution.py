import sys
from functools import reduce
from operator import add, mul


def main():
    filename = sys.argv[1]
    with open(filename) as worksheet_file:
        worksheet_raw = worksheet_file.read().splitlines()

    num_problems = len(worksheet_raw[0].split())
    worksheet_operands = [[] for _ in range(num_problems)]
    for line in worksheet_raw[:-1]:
        for i, op in enumerate(int(o) for o in line.split()):
            worksheet_operands[i].append(op)
    
    worksheet_operators = worksheet_raw[-1].split()
    total = 0
    for i, operands in enumerate(worksheet_operands):
        operator = add if worksheet_operators[i] == '+' else mul
        total += reduce(operator, operands)

    print(total)


if __name__ == '__main__':
    main()
