import sys
import re
from collections import defaultdict

LABEL_PATTERN = re.compile(r'([a-z]+)([=\-])(\d*)')


def string_hash(step: str) -> int:
    current_value = 0
    for char in step:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def main():
    filename = sys.argv[1]
    with open(filename) as initialization_sequence_file:
        initialization_sequence = initialization_sequence_file.read().split(',')

    boxes = defaultdict(list)
    for step in initialization_sequence:
        step_parts = LABEL_PATTERN.search(step)
        label, operation = step_parts.group(1), step_parts.group(2)
        box = string_hash(label)

        if operation == '=':
            focal_length = int(step_parts.group(3))

            if label in [l for l, _ in boxes[box]]:
                lens_idx = [i for i in range(len(boxes[box]))
                            if boxes[box][i][0] == label][0]
                boxes[box][lens_idx] = (label, focal_length)
            else:
                boxes[box].append((label, focal_length))

        else:
            if label in [l for l, _ in boxes[box]]:
                lens = [l for l in boxes[box] if l[0] == label][0]
                boxes[box].remove(lens)

    total_focusing_power = 0
    for box, lenses in boxes.items():
        for i, lens in enumerate(lenses):
            total_focusing_power += (box+1) * (i+1) * lens[1]

    print(total_focusing_power)


if __name__ == '__main__':
    main()
