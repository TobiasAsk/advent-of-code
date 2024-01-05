import sys


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
    print(sum(string_hash(step.strip()) for step in initialization_sequence))


if __name__ == '__main__':
    main()
