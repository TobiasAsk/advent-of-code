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

    def run_program(self):
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

        print(','.join(str(o) for o in self.output))


def parse_register(register_info_line: str) -> tuple[str, int]:
    match = REGISTER_PATTERN.search(register_info_line)
    return match.group(1), int(match.group(2))


def main():
    filename = sys.argv[1]
    with open(filename) as program_info_file:
        register_info, program_instructions = program_info_file.read().split('\n\n')

    register_values = dict(parse_register(r) for r in register_info.splitlines())
    program_instructions = [int(n) for n in DIGIT_PATTERN.findall(program_instructions)]
    computer = Computer(register_values, program_instructions)
    computer.run_program()
    f = 2


if __name__ == '__main__':
    main()
