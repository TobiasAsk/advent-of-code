"""
Use a pulse queue. Had to inspect the input to see that the rx module has a single conjunction module as input,
which I assume is always the case. For this module, we can find the individual cycle lengths for its inputs.
The total number of required button presses is then the LCM of these cycle lenghts.
"""

import sys
from dataclasses import dataclass, field
from collections import namedtuple, deque
import pygraphviz as pgv
import math


Pulse = namedtuple('Pulse', ['is_high', 'source', 'destination'])


@dataclass
class NoOpModule:
    destination_modules: list[str] = field(default_factory=list)

    def receive_pulse(self, is_high: bool, input_module):
        return None


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


def parse(input: list[str]) -> tuple[dict, ConjunctionModule]:
    modules = {}
    conjunction_module_names = []
    final_conjunction_module = None
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

        if 'rx' in destination_modules:
            final_conjunction_module = module

    for line in input:
        source_module, destination_modules = line.split('->')
        source_module = source_module.strip()
        destination_modules = [m.strip() for m in destination_modules.split(',')]

        for destination_module in destination_modules:
            if destination_module in conjunction_module_names:
                conjunction_module = modules[destination_module]
                conjunction_module.input_pulses[source_module[1:]] = False

            if destination_module not in modules:
                modules[destination_module] = NoOpModule()

    return modules, final_conjunction_module


def draw_graph(modules: dict):
    graph = pgv.AGraph(directed=True, overlap='scale')
    for module_name, module in modules.items():
        shape = 'ellipse' if isinstance(module, FlipFlopModule) else 'box' if isinstance(
            module, ConjunctionModule) else 'diamond' if isinstance(module, BroadcasterModule) else 'box3d'
        graph.add_node(module_name, shape=shape)

        for destination_module in module.destination_modules:
            graph.add_edge(module_name, destination_module)

    print(f'{len(graph.nodes())}')
    graph.layout(prog='neato')
    graph.draw('graph.png')


def main():
    filename = sys.argv[1]
    with open(filename) as something_file:
        modules, final_conjunction_module = parse(something_file.read().splitlines())

    # draw_graph(modules)
    first_high = {}
    cycle_lengths = {}
    has_been_high = {m: False for m in final_conjunction_module.input_pulses}
    done = False
    num_button_presses = 0

    while not done:
        num_button_presses += 1
        first_pulse = Pulse(is_high=False, source='button', destination='broadcaster')
        pulse_queue = deque([first_pulse])

        while pulse_queue:
            pulse = pulse_queue.popleft()
            destination_module = modules[pulse.destination]

            if destination_module == final_conjunction_module and pulse.is_high:
                if not has_been_high[pulse.source]:
                    has_been_high[pulse.source] = True
                    first_high[pulse.source] = num_button_presses
                else:
                    cycle_length = num_button_presses - first_high[pulse.source]
                    cycle_lengths[pulse.source] = cycle_length
                    if len(cycle_lengths) == 4:
                        done = True
                        break

            new_pulse_type = destination_module.receive_pulse(pulse.is_high, pulse.source)
            if new_pulse_type != None:
                for module in destination_module.destination_modules:
                    new_pulse = Pulse(is_high=new_pulse_type, source=pulse.destination, destination=module)
                    pulse_queue.append(new_pulse)

    num_presses_required = math.lcm(*cycle_lengths.values())
    print(num_presses_required)


if __name__ == '__main__':
    main()
