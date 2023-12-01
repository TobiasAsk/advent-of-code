def get_stacks(crates):
    # stacks are always 3 chars wide, regardless of height
    num_stacks = len(crates[0]) // 3
    stacks = [[] for _ in range(num_stacks)]

    for crate_row in crates:
        for i in range(0, len(crate_row), 4):
            if crate_row[i] == '[':
                stack = i // 4
                stacks[stack].insert(0, crate_row[i+1])

    return stacks


def parse_move(move):
    parts = move.split()
    return int(parts[1]), int(parts[3]) - 1, int(parts[5]) - 1


def apply_move(move, stacks):
    num_crates, src, dest = move
    new_stacks = [[c for c in stack] for stack in stacks]

    for _ in range(num_crates):
        crate = new_stacks[src].pop()
        new_stacks[dest].append(crate)

    return new_stacks


def main():
    with open('dag 5/example_input.txt') as crates_and_procedures_file:
        crates_and_procedures = crates_and_procedures_file.read().splitlines()

    crates = [line for line in crates_and_procedures if line.startswith(
        '[') or line.startswith('  ')]

    moves = [parse_move(line)
             for line in crates_and_procedures if line.startswith('move')]

    stacks = get_stacks((crates))
    for move in moves:
        stacks = apply_move(move, stacks)

    print(stacks)


if __name__ == '__main__':
    main()
