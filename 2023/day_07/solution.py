import sys
from dataclasses import dataclass

CARD_STRENGTHS = 'AKQJT98765432'


@dataclass
class Hand:
    cards: str

    @property
    def type(self):
        counts = {c: self.cards.count(c) for c in self.cards}
        vals = counts.values()
        if 5 in vals:
            return 7
        elif 4 in vals:
            return 6
        elif 3 in vals and 2 in vals:
            return 5
        elif 3 in vals:
            return 4
        elif list(vals).count(2) == 2:
            return 3
        elif 2 in vals:
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
    main()
