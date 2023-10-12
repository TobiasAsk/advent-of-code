import sys

DIRECTIONS = [
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0),  # left
    (0, -1)  # up
]


def parse_notes(notes):
    max_width = 0
    board_map = []

    for row in notes[:-2]:
        board_map.append(row)
        max_width = max(max_width, len(row))

    board_map = [row if len(row) == max_width else row +
                 ' ' * (max_width-len(row)) for row in board_map]

    raw_path: str = notes[-1]
    path = []
    i = 0

    while i < len(raw_path):
        if raw_path[i].isdigit():
            digit_start = i
            while i < len(raw_path) and raw_path[i].isdigit():
                i += 1
            path.append(int(raw_path[digit_start:i]))
        else:
            path.append(raw_path[i])
            i += 1

    start_x = [i for i in range(len(board_map[0]))
               if board_map[0][i] == '.'][0]
    return board_map, path, (start_x, 0)


def print_board(board_map, position):
    x, y = position
    for row in range(len(board_map)):
        out_row = ''.join(['P' if i == x and row == y else board_map[row][i]
                           for i in range(len(board_map[row]))])
        print(out_row)
    print()


def move(num_steps, facing, position, board_map) -> int:
    max_width, max_height = len(board_map[0]), len(board_map)
    d_x, d_y = DIRECTIONS[facing]
    x, y = position

    for _ in range(num_steps):
        new_x = x + d_x
        new_y = y + d_y
        wrap = False

        if (0 <= new_x < max_width and 0 <= new_y < max_height):
            if board_map[new_y][new_x] == '.':
                x = new_x
                y = new_y

            elif board_map[new_y][new_x] == ' ':
                wrap = True

        else:
            wrap = True
                    
        if wrap:
            opposite_d_x, opposite_d_y = DIRECTIONS[(facing+2) % 4]

            while (0 <= new_x + opposite_d_x < max_width and 0 <= new_y + opposite_d_y < max_height and
                    board_map[new_y+opposite_d_y][new_x+opposite_d_x] != ' '):
                new_x += opposite_d_x
                new_y += opposite_d_y

            if board_map[new_y][new_x] == '.':
                x = new_x
                y = new_y
            else:
                break

        position = (x, y)

    return position


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        notes = map_file.read().splitlines()

    board_map, path, position = parse_notes(notes)
    facing = 0

    for instruction in path:
        if isinstance(instruction, int):
            position = move(instruction, facing, position, board_map)

        else:
            rotation = 1 if instruction == 'R' else -1
            facing = (facing + rotation) % 4

    x, y = position
    password = 1000 * (y+1) + 4 * (x+1) + facing
    print(f'Password is {password}')


if __name__ == '__main__':
    main()
