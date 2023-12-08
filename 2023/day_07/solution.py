import sys
from dataclasses import dataclass

CARD_STRENGTHS = 'AKQT98765432J'


@dataclass
class Hand:
    cards: str

    @property
    def type(self):
        non_joker_counts = [self.cards.count(c) for c in set(self.cards) if c != 'J']
        num_jokers = self.cards.count('J')
        if any(c+num_jokers == 5 for c in non_joker_counts) or num_jokers == 5:
            return 7
        elif any(c+num_jokers == 4 for c in non_joker_counts):
            return 6
        elif ((3 in non_joker_counts and 2 in non_joker_counts)
              or (list(non_joker_counts).count(2) == 2 and num_jokers == 1)):  # ordinary full house or with a joker. More jokers than 1 would lead to a better hand
            return 5
        elif any(c+num_jokers == 3 for c in non_joker_counts):
            return 4
        elif list(non_joker_counts).count(2) == 2:
            return 3
        elif any(c+num_jokers == 2 for c in non_joker_counts):
            return 2
        return 1

    def __lt__(self, other):
        if self.type < other.type:
            return True
        elif self.type > other.type:
            return False
        else:
            for i in range(5):
                strength_diff = CARD_STRENGTHS.index(self.cards[i]) - CARD_STRENGTHS.index(other.cards[i])
                if strength_diff != 0:
                    return strength_diff > 0


def main():
    filename = sys.argv[1]
    hands = []
    with open(filename) as hands_file:
        for line in hands_file:
            cards, bid = line.split()
            hands.append((Hand(cards), int(bid)))

    sorted_hands = sorted(hands)
    total_winnings = sum(sorted_hands[i][1]*(i+1) for i in range(len(sorted_hands)))
    print(total_winnings)


if __name__ == '__main__':
    five_of_a_kind = Hand('55555')
    for i in range(6):
        five_of_a_kind.cards = five_of_a_kind.cards.replace('5', 'J', i)
        assert five_of_a_kind.type == 7

    main()
