import sys
import re

REGISTER_PATTERN = re.compile(r'Register ([ABC]): (\d+)')
DIGIT_PATTERN = re.compile(r'\d')


class Computer:
    def __init__(self, register_values: dict[str, int], program: list[int]):
        self.register_values = register_values
        self.program = program
        self.instruction_pointer = 0
        self.output = []

    def read_combo_operand(self):
        operand = self.program[self.instruction_pointer+1]
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.register_values['A']
        if operand == 5:
            return self.register_values['B']
        if operand == 6:
            return self.register_values['C']

    def run_program(self, print_output=True):
        self.instruction_pointer = 0
        self.output = []

        while self.instruction_pointer < len(self.program):
            opcode = self.program[self.instruction_pointer]
            should_increment = True
            if opcode == 0:
                operand = self.read_combo_operand()
                self.register_values['A'] = int(self.register_values['A']/(2**operand))
            if opcode == 1:
                operand = self.program[self.instruction_pointer+1]
                self.register_values['B'] = self.register_values['B'] ^ operand
            if opcode == 2:
                value = self.read_combo_operand()
                self.register_values['B'] = value % 8
            if opcode == 3:
                if self.register_values['A'] != 0:
                    operand = self.program[self.instruction_pointer+1]
                    self.instruction_pointer = operand
                    should_increment = False
            if opcode == 4:
                self.register_values['B'] = self.register_values['B'] ^ self.register_values['C']
            if opcode == 5:
                operand = self.read_combo_operand()
                self.output.append(operand % 8)
            if opcode == 6:
                operand = self.read_combo_operand()
                self.register_values['B'] = int(self.register_values['A']/(2**operand))
            if opcode == 7:
                operand = self.read_combo_operand()
                self.register_values['C'] = int(self.register_values['A']/(2**operand))

            if should_increment:
                self.instruction_pointer += 2

        if print_output:
            print(','.join(str(o) for o in self.output))

    def search(self, register_value: str, idx: int = 0):
        base_ten_value = int(register_value, 8)
        self.register_values = {
            'A': base_ten_value,
            'B': 0,
            'C': 0
        }
        self.run_program(print_output=False)
        if self.output == self.program:
            print(base_ten_value)

        comp_idx = 15 - idx
        if self.output[comp_idx:] != self.program[comp_idx:]:
            return

        extension = first_extension(register_value, idx)
        while extension != None:
            self.search(*extension)
            extension = next_extension(*extension)


def next_extension(register_value: str, idx: int) -> tuple[str, int]:
    digit = int(register_value[idx])
    threshold = 1 if idx == 0 else 0

    if digit > threshold:
        return (register_value[:idx] + str(digit-1) + register_value[idx+1:], idx)

    if idx == 15:
        return None

    next_digit = int(register_value[idx+1])
    return (register_value[:idx+1] + str(next_digit-1) + register_value[idx+2:], idx+1)


def first_extension(register_value: str, idx: int) -> tuple[str, int]:
    return (register_value, idx+1) if idx < 15 else None


def parse_register(register_info_line: str) -> tuple[str, int]:
    match = REGISTER_PATTERN.search(register_info_line)
    return match.group(1), int(match.group(2))


def main():
    filename = sys.argv[1]
    with open(filename) as program_info_file:
        register_info, program_instructions = program_info_file.read().split('\n\n')

    program_instructions = [int(n) for n in DIGIT_PATTERN.findall(program_instructions)]
    register_values = {'B': 0, 'C': 0}
    computer = Computer(register_values, program_instructions)
    computer.search('7777777777777777')


if __name__ == '__main__':
    main()
