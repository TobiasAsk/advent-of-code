import sys


WORD_TO_DIGIT = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


DIGITS = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
          'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def main():
    filename = sys.argv[1]
    calibration_value_sum = 0
    with open(filename) as calibration_document:
        for line in calibration_document:
            indices_first = [(i, d) for d in DIGITS if (i := line.find(d)) >= 0]
            indices_last = [(i, d) for d in DIGITS if (i := line.rfind(d)) >= 0]
            _, first_digit = min(indices_first)
            _, last_digit = max(indices_last)

            first_digit = WORD_TO_DIGIT.get(first_digit, first_digit)
            last_digit = WORD_TO_DIGIT.get(last_digit, last_digit)
            calibration_value_sum += int(first_digit + last_digit)

    print(f'Sum is {calibration_value_sum}')


if __name__ == '__main__':
    main()
