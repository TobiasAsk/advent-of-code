import sys
import functools
import math
from dataclasses import dataclass, field
import re


BUTTON_PATTERN = re.compile(r'Button [AB]: X\+(\d+), Y\+(\d+)')
PRIZE_PATTERN = re.compile(r'Prize: X=(\d+), Y=(\d+)')


@dataclass(frozen=True)
class ClawMachine:
    button_a_num_units: tuple[int]  # = field(hash=True)
    button_b_num_units: tuple[int]  # = field(hash=True)
    prize_location: tuple[int]

    @functools.cache
    def get_min_price(
            self,
            pos: tuple[int],
            num_presses_left: tuple[int]):

        if pos == self.prize_location:
            return 0

        if pos[0] > self.prize_location[0] or pos[1] > self.prize_location[1]:
            return math.inf

        press_a_option = 3 + self.get_min_price(
            (pos[0]+self.button_a_num_units[0], pos[1]+self.button_a_num_units[1]),
            (num_presses_left[0]-1, num_presses_left[1])
        ) if num_presses_left[0] > 0 else math.inf

        press_b_option = 1 + self.get_min_price(
            (pos[0]+self.button_b_num_units[0], pos[1]+self.button_b_num_units[1]),
            (num_presses_left[0], num_presses_left[1]-1)
        ) if num_presses_left[1] > 0 else math.inf

        return min(press_a_option, press_b_option)


def main():
    filename = sys.argv[1]

    min_price = 0
    with open(filename) as claw_machine_configs_file:
        for machine_config in claw_machine_configs_file.read().split('\n\n'):
            button_units = BUTTON_PATTERN.findall(machine_config)
            prize_location_coords = PRIZE_PATTERN.search(machine_config).groups()
            machine = ClawMachine(
                button_a_num_units=tuple(map(int, button_units[0])),
                button_b_num_units=tuple(map(int, button_units[1])),
                prize_location=tuple(map(int, prize_location_coords))
            )
            machine_min_price = machine.get_min_price(
                pos=(0, 0),
                num_presses_left=(100, 100)
            )
            min_price += machine_min_price if machine_min_price < math.inf else 0

    print(min_price)


if __name__ == '__main__':
    main()
