import sys
from enum import Enum
from functools import cache
import math

NUMERIC_KEYPAD = (
    '789',
    '456',
    '123',
    'X0A'
)

DIRECTIONAL_KEYPAD = (
    'X^A',
    '<v>'
)


class Direction(Enum):
    Right = (1, 0)
    Down = (0, 1)
    Left = (-1, 0)
    Up = (0, -1)


DIRECTION_SYMBOLS = {
    Direction.Right: '>',
    Direction.Down: 'v',
    Direction.Left: '<',
    Direction.Up: '^'
}

DIRECTIONS = [Direction.Right, Direction.Down, Direction.Left, Direction.Up]


def get_position(key: str, keypad: tuple[str]) -> tuple[int, int]:
    height, width = len(keypad), len(keypad[0])
    return [(x, y) for x in range(width) for y in range(height)
            if keypad[y][x] == key][0]


def manhattan_dist(pos: tuple[int, int], other_pos: tuple[int, int]) -> int:
    return abs(pos[0]-other_pos[0]) + abs(pos[1]-other_pos[1])


@cache
def get_all_shortest_sequences(keypad: tuple[str], from_button: str, to_button: str, current_sequence: str = ''):
    if from_button == to_button:
        return ['']
    height, width = len(keypad), len(keypad[0])
    from_key_position = get_position(from_button, keypad)
    to_key_position = get_position(to_button, keypad)
    distance_to_target = manhattan_dist(from_key_position, to_key_position)
    x, y = from_key_position

    sequences = []
    for direction in DIRECTIONS:
        dx, dy = direction.value
        if 0 <= x+dx < width and 0 <= y+dy < height:
            new_key = keypad[y+dy][x+dx]
            if new_key == to_button:
                return current_sequence + DIRECTION_SYMBOLS[direction]
            elif new_key != 'X' and manhattan_dist((x+dx, y+dy), to_key_position) < distance_to_target:
                res = get_all_shortest_sequences(keypad, new_key, to_button,
                                                 current_sequence+DIRECTION_SYMBOLS[direction])
                if isinstance(res, str):
                    sequences.append(res)
                else:
                    sequences.extend(res)
    return sequences


@cache
def get_all_shortest_sequences_for_code(keypad: tuple[str], code: str, current_sequence: str = ''):
    if len(code) == 1:
        return current_sequence

    sequences = []
    for continuation in get_all_shortest_sequences(keypad, code[0], code[1]):
        res = get_all_shortest_sequences_for_code(keypad, code[1:], current_sequence+continuation+'A')
        if isinstance(res, str):
            sequences.append(res)
        else:
            sequences.extend(res)

    return sequences


class RobotChain:

    def __init__(self) -> None:
        self.best = {}

    @cache
    def find_optimal_sequence_length(self, current_sequence: str, depth: int = 0):
        if depth == 3:
            if len(current_sequence) < self.best.get(depth, math.inf):
                self.best[depth] = len(current_sequence)
            return self.best[depth]

        if len(current_sequence) > self.best.get(depth+1, math.inf):
            return math.inf

        keypad = NUMERIC_KEYPAD if depth == 0 else DIRECTIONAL_KEYPAD
        options = get_all_shortest_sequences_for_code(keypad, code='A'+current_sequence)
        sequence_lengths = [self.find_optimal_sequence_length(option, depth=depth+1) for option in options]
        min_length = min(sequence_lengths)
        self.best[depth] = min_length
        return min_length


def test():
    sequences = get_all_shortest_sequences_for_code(NUMERIC_KEYPAD, 'A029A')
    assert '<A^A>^^AvvvA' in sequences
    options = get_all_shortest_sequences_for_code(DIRECTIONAL_KEYPAD, 'A<')
    print('tests pass')


def main():
    filename = sys.argv[1]

    with open(filename) as code_file:
        for code in code_file.read().splitlines():
            robot_chain = RobotChain()
            minimal = robot_chain.find_optimal_sequence_length(code)
            print(minimal)


if __name__ == '__main__':
    test()
    main()
