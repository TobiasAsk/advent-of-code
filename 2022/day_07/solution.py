from dataclasses import dataclass, field


@dataclass
class Node:
    is_directory: bool
    size: int = 0
    children: list = field(default_factory=list)
    parent: object = None
    name: str = ''


def recursive_visit(node: Node, sizes_under_limit):
    if node.size < 100000:
        sizes_under_limit.append(node.size)
    for child in [c for c in node.children if c.is_directory]:
        recursive_visit(child, sizes_under_limit)


def recursive_visit2(node: Node, sizes_under_limit: list, missing: int):
    if node.size > missing:
        sizes_under_limit.append(node.size)
    for child in [c for c in node.children if c.is_directory]:
        recursive_visit2(child, sizes_under_limit, missing)


def part1(root: Node):
    sizes_under_limit = []
    recursive_visit(root, sizes_under_limit)
    return sum(sizes_under_limit)


def part2(root: Node):
    free_space = 70000000 - root.size
    missing = 30000000 - free_space
    sizes_over_limit = []
    recursive_visit2(root, sizes_over_limit, missing)
    return min(sizes_over_limit)


def bubble_size(node: Node, file_size):
    current_node = node
    current_node.size += file_size

    while current_node.parent != None:
        current_node = current_node.parent
        current_node.size += file_size


def parse_file_system(terminal_output):
    root = Node(name='/', is_directory=True)
    current_directory = root

    for line in map(str.rstrip, terminal_output):
        parts = line.split()
        if parts[0] == '$':
            if parts[1] == 'cd':
                new_dir_name = parts[2]
                if new_dir_name == '/':
                    current_directory = root
                elif new_dir_name == '..' and current_directory.name != '/':
                    current_directory = current_directory.parent
                else:
                    target = [
                        c for c in current_directory.children if c.name == new_dir_name]
                    if len(target) == 1:
                        current_directory = target[0]

        else:
            if parts[0] == 'dir':
                child = Node(
                    name=parts[1], parent=current_directory, is_directory=True)

            else:
                file_size = int(parts[0])
                child = Node(size=file_size, name=parts[1], is_directory=False)
                bubble_size(current_directory, file_size)

            current_directory.children.append(child)

    return root


def main():
    with open('dag 7/input.txt') as terminal_output:
        root = parse_file_system(terminal_output)

    solution = part1(root)
    print(f'Sum is {solution}')

    solution_part2 = part2(root)
    print(f'part 2 {solution_part2}')

if __name__ == '__main__':
    main()
