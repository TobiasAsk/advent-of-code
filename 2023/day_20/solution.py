import sys
from dataclasses import dataclass, field
from collections import namedtuple, deque

Pulse = namedtuple('Pulse', ['is_high', 'source', 'destination'])


@dataclass
class BroadcasterModule:
    destination_modules: list[str] = field(default_factory=list)

    def receive_pulse(self, is_high: bool, input_module):
        return is_high


@dataclass
class FlipFlopModule:
    is_on: bool = False
    destination_modules: list[str] = field(default_factory=list)

    def receive_pulse(self, is_high: bool, input_module):
        if is_high:
            return None

        out_pulse = not self.is_on
        self.is_on = not self.is_on
        return out_pulse


@dataclass
class ConjunctionModule:
    input_pulses: dict[str, bool] = field(default_factory=dict)
    destination_modules: list[str] = field(default_factory=list)

    def receive_pulse(self, is_high: bool, input_module: str):
        self.input_pulses[input_module] = is_high
        out_pulse = not all(p == True for p in self.input_pulses.values())
        return out_pulse


def parse(input: list[str]):
    modules = {}
    conjunction_module_names = []
    for line in input:
        source_module, destination_modules = line.split('->')
        source_module = source_module.strip()
        destination_modules = [m.strip() for m in destination_modules.split(',')]
        name = source_module[1:]

        if source_module.startswith('%'):
            module = FlipFlopModule(destination_modules=destination_modules)
        elif source_module.startswith('&'):
            module = ConjunctionModule(destination_modules=destination_modules)
            conjunction_module_names.append(name)
        elif source_module == 'broadcaster':
            module = BroadcasterModule(destination_modules=destination_modules)
            name = source_module

        modules[name] = module

    for line in input:
        source_module, destination_modules = line.split('->')
        source_module = source_module.strip()
        destination_modules = [m.strip() for m in destination_modules.split(',')]

        for destination_module in destination_modules:
            if destination_module in conjunction_module_names:
                conjunction_module = modules[destination_module]
                conjunction_module.input_pulses[source_module[1:]] = False

    return modules


def main():
    filename = sys.argv[1]
    with open(filename) as something_file:
        modules = parse(something_file.read().splitlines())

    num_low_pulses = num_high_pulses = 0
    for _ in range(1000):
        first_pulse = Pulse(is_high=False, source='button', destination='broadcaster')
        pulse_queue = deque([first_pulse])
        while pulse_queue:
            pulse = pulse_queue.popleft()

            if pulse.is_high:
                num_high_pulses += 1
            else:
                num_low_pulses += 1

            if pulse.destination not in modules:
                continue

            destination_module = modules[pulse.destination]
            new_pulse_type = destination_module.receive_pulse(pulse.is_high, pulse.source)
            if new_pulse_type != None:
                for module in destination_module.destination_modules:
                    new_pulse = Pulse(is_high=new_pulse_type, source=pulse.destination, destination=module)
                    pulse_queue.append(new_pulse)

    product = num_low_pulses * num_high_pulses
    print(product)


if __name__ == '__main__':
    main()
