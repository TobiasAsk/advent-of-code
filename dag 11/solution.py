from dataclasses import dataclass, field
from functools import reduce
from operator import mul
from collections import deque


@dataclass
class Monkey:
    operation: str
    divisor: int
    throws_to: tuple[int, int]
    items: deque = field(default_factory=deque)
    num_inspections: int = 0


def parse_monkeys(monkey_specs) -> list[Monkey]:
    monkeys = []
    for i in range(0, len(monkey_specs), 7):
        items = [int(item)
                 for item in monkey_specs[i+1].split(':')[1].split(',')]

        operation = monkey_specs[i+2].split('=')[1].strip()

        divisor = int(monkey_specs[i+3].split()[-1])
        throws_to = (int(monkey_specs[i+4].split()[-1]),
                     int(monkey_specs[i+5].split()[-1]))

        monkey = Monkey(operation=operation,
                        divisor=divisor, throws_to=throws_to)
        for item in items:
            monkey.items.append(item)

        monkeys.append(monkey)

    return monkeys


def part2():
    with open('dag 11/input.txt') as monkey_specs_file:
        monkeys = parse_monkeys(monkey_specs_file.readlines())

    divisors = [monkey.divisor for monkey in monkeys]
    least_common_multiple = reduce(mul, divisors)

    for _ in range(10000):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                monkey.num_inspections += 1
                item = monkey.items.popleft()
                worry_level = eval(monkey.operation, {}, {'old': item }) % least_common_multiple

                throw_to = (monkey.throws_to[0] if worry_level % monkey.divisor == 0
                            else monkey.throws_to[1])
                monkeys[throw_to].items.append(worry_level)

    num_inspections_per_monkey = [monkey.num_inspections for monkey in monkeys]
    sorted_num_inspections = sorted(num_inspections_per_monkey)
    top_two = sorted_num_inspections[-2:]
    monkey_business_level = reduce(mul, top_two)
    print(monkey_business_level)


# def part1():
#     with open('dag 11/input.txt') as monkey_specs_file:
#         monkeys = parse_monkeys(monkey_specs_file.readlines())

#     for _ in range(20):
#         for monkey in monkeys:
#             while len(monkey.items) > 0:
#                 monkey.num_inspections += 1
#                 item = monkey.items.pop(0)
#                 worry_level = eval(monkey.operation, {}, {'old': item})
#                 worry_level = worry_level // 3
#                 throw_to = (monkey.throws_to[0] if worry_level % monkey.divisor == 0
#                             else monkey.throws_to[1])
#                 monkeys[throw_to].items.append(worry_level)

#     num_inspections_per_monkey = [monkey.num_inspections for monkey in monkeys]
#     sorted_num_inspections = sorted(num_inspections_per_monkey)
#     top_two = sorted_num_inspections[-2:]
#     monkey_business_level = reduce(mul, top_two)
#     print(monkey_business_level)


if __name__ == '__main__':
    part2()
