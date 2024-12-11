import sys
import re

EQUATION_PATTERN = re.compile(r'(\d+): ([\d+ ]+)')


def parse_equation_line(equation_line):
    m = EQUATION_PATTERN.search(equation_line)
    return int(m.group(1)), list(map(int, m.group(2).split()))


def can_make_value(value, operands) -> bool:
    if len(operands) == 1:
        return operands[0] == value

    elif operands[0] > value:
        return False

    add_option = [operands[0] + operands[1]] + operands[2:]
    mul_option = [operands[0] * operands[1]] + operands[2:]
    concat_option = [int(''.join(map(str, operands[:2])))] + operands[2:]

    if can_make_value(value, operands=add_option):
        return True

    if can_make_value(value, operands=mul_option):
        return True
    
    if can_make_value(value, operands=concat_option):
        return True

    return False


def main():
    filename = sys.argv[1]
    with open(filename) as equations_file:
        equations = equations_file.read().splitlines()

    value_sum = 0
    for equation in equations:
        value, operands = parse_equation_line(equation)
        if can_make_value(value, operands):
            value_sum += value

    print(value_sum)


if __name__ == '__main__':
    main()
