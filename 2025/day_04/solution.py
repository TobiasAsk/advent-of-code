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
    num_accessible = 0
    for y in range(1, height):
        for x in range(1, width):
            if roll_diagram[y][x] == '@':
                neighbors = [roll_diagram[y+dy][x+dx] for dy in range(-1, 2) for dx in range(-1, 2)
                             if (dx, dy) != (0, 0) and roll_diagram[y+dy][x+dx] == '@']
                num_accessible += len(neighbors) < 4
    print(num_accessible)


if __name__ == '__main__':
    main()
