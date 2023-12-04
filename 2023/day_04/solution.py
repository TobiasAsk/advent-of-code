import sys


def get_num_winning_numbers(card_line):
    parts = card_line.split('|')
    winning_numbers = set(int(n) for n in parts[0].split(':')[1].split())
    my_numbers = set(int(n) for n in parts[1].split())
    return len(winning_numbers & my_numbers)


def main():
    filename = sys.argv[1]

    with open(filename) as scratchcard_file:
        card_lines = scratchcard_file.readlines()

    cards = [1] * len(card_lines)
    for card_num, card_line in enumerate(card_lines):
        num_winning_nums = get_num_winning_numbers(card_line)
        for i in range(card_num+1, card_num+1+num_winning_nums):
            cards[i] += cards[card_num]

    print(sum(cards))


if __name__ == '__main__':
    main()
