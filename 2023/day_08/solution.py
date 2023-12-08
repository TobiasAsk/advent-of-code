import sys
import re
import math

CHILDREN_PATTERN = re.compile(r'[A-Z1-2]{3}')
DIRECTIONS = 'LR'


def get_num_required_steps(
        start_node: str,
        instructions: str,
        network: dict[str, list[str]]):

    current_node = start_node
    num_steps = 0
    while not current_node.endswith('Z'):
        instruction = instructions[num_steps % len(instructions)]
        direction = DIRECTIONS.index(instruction)
        current_node = network[current_node][direction]
        num_steps += 1
    return num_steps


def main():
    filename = sys.argv[1]
    with open(filename) as nav_docs_file:
        nav_docs = nav_docs_file.read().splitlines()

    instructions = nav_docs[0]
    network: dict[str, list[str]] = {}
    for line in nav_docs[2:]:
        node, children = line.split('=')
        network[node.strip()] = CHILDREN_PATTERN.findall(children)

    start_nodes = [n for n in network if n.endswith('A')]
    required_individual_steps = [get_num_required_steps(n, instructions, network) for n in start_nodes]
    required_steps = math.lcm(*required_individual_steps)
    print(required_steps)


if __name__ == '__main__':
    main()
