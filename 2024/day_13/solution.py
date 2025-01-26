'''System of two equations to solve. Just use numpy, but feels like cheating. Only looking
for integer solutions, so needs a check using the rounded solution.
'''

import sys
import re
import numpy as np


BUTTON_PATTERN = re.compile(r'Button [AB]: X\+(\d+), Y\+(\d+)')
PRIZE_PATTERN = re.compile(r'Prize: X=(\d+), Y=(\d+)')


def main():
    filename = sys.argv[1]

    min_price = 0
    with open(filename) as claw_machine_configs_file:
        for machine_config in claw_machine_configs_file.read().split('\n\n'):
            button_a, button_b = BUTTON_PATTERN.findall(machine_config)
            prize_location_coords = PRIZE_PATTERN.search(machine_config).groups()
            coefficients = np.array([
                [int(button_a[0]), int(button_b[0])],
                [int(button_a[1]), int(button_b[1])]
            ])
            offset = 10000000000000
            ordinate_values = np.array([
                int(prize_location_coords[0])+offset,
                int(prize_location_coords[1])+offset,
            ])
            solution = np.linalg.solve(a=coefficients, b=ordinate_values)

            if all(np.round(solution[0])*coefficients[i][0] +
                   np.round(solution[1])*coefficients[i][1] == ordinate_values[i]
                   for i in range(2)):
                min_price += 3*solution[0] + solution[1]

    print(min_price)


if __name__ == '__main__':
    main()
