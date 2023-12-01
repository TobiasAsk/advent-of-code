def part2():
    with open('dag 10/input.txt') as program:
        instructions = program.read().splitlines()

    i = 0
    cycle_number = register_value = 1
    executing = False

    while i < len(instructions):
        crt_pos = (cycle_number - 1) % 40
        pixel = ('#' if register_value - 1 <= crt_pos <=
                 register_value + 1 else '.')
        line_end = '\n' if cycle_number % 40 == 0 else ''
        print(pixel, end=line_end)

        instruction = instructions[i]
        if instruction == 'noop':
            i += 1
        else:
            if executing:
                executing = False
                register_value += int(instruction.split()[1])
                i += 1

            else:
                executing = True

        cycle_number += 1


def part1():
    with open('dag 10/input.txt') as program:
        instructions = program.read().splitlines()

    i = 0
    cycle_number = register_value = 1
    executing = False
    signal_strength_sums = 0
    while i < len(instructions):
        if (cycle_number - 20) % 40 == 0:
            signal_strength_sums += register_value * cycle_number

        instruction = instructions[i]
        if instruction == 'noop':
            i += 1
        else:
            if executing:
                register_value += int(instruction.split()[1])
                executing = False
                i += 1

            else:
                executing = True

        cycle_number += 1

    print(signal_strength_sums)


if __name__ == '__main__':
    # part1()
    part2()
