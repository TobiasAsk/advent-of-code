import sys


def main():
    filename = sys.argv[1]
    total_points = 0
    with open(filename) as scratchcard_file:
        for card_line in scratchcard_file:
            parts = card_line.split('|')
            winning_numbers = set(int(n) for n in parts[0].split(':')[1].split())
            my_numbers = set(int(n) for n in parts[1].split())
            num_winning_numbers = len(winning_numbers & my_numbers)
            if num_winning_numbers > 0:
                total_points += 2**(num_winning_numbers-1)
    print(total_points)


if __name__ == '__main__':
    main()
