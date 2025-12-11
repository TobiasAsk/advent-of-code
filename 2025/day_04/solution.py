import sys


def add_padding(roll_diagram: list[str]) -> list[str]:
    height, width = len(roll_diagram), len(roll_diagram[0])
    new_diagram = ['.'*(width+2)]
    for row in roll_diagram:
        new_row = '.' + row + '.'
        new_diagram.append(new_row)
    new_diagram.append('.'*(width+2))
    return new_diagram


def main():
    filename = sys.argv[1]
    with open(filename) as diagram_file:
        roll_diagram = diagram_file.read().splitlines()

    roll_diagram = add_padding(roll_diagram)
    height, width = len(roll_diagram), len(roll_diagram[0])
    removing = True
    total_removed = 0
    
    while removing:
        removing = False
        new_diagram = [r for r in roll_diagram]
        for y in range(1, height):
            for x in range(1, width):
                if roll_diagram[y][x] == '@':
                    neighbors = [roll_diagram[y+dy][x+dx] for dy in range(-1, 2) for dx in range(-1, 2)
                                 if (dx, dy) != (0, 0) and roll_diagram[y+dy][x+dx] == '@']

                    if len(neighbors) < 4:
                        new_diagram[y] = new_diagram[y][:x] + 'x' + new_diagram[y][x+1:]
                        removing = True
                        total_removed += 1

        roll_diagram = [r for r in new_diagram]

    print(total_removed)


if __name__ == '__main__':
    main()
