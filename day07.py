from collections import Counter

from loader import load_strs


class Card:
    def __init__(self, label, jokers=False):
        self.label = label
        self.strength = {str(x): x for x in range(2, 10)}
        self.strength["T"] = 10
        self.strength["J"] = 1 if jokers else 11
        self.strength["Q"] = 12
        self.strength["K"] = 13
        self.strength["A"] = 14

    def __repr__(self):
        return self.label

    def __ne__(self, other):
        return self.strength[self.label] != self.strength[other.label]

    def __lt__(self, other):
        return self.strength[self.label] < self.strength[other.label]


class Hand:
    def __init__(self, cards, bid, jokers=False):
        self.jokers = jokers
        self.cards = [Card(label, jokers) for label in cards]
        self.counted_cards = Counter(cards)
        self.counted_cards_jokers = Counter(cards)
        self.account_for_jokers()
        self.get_hand_type()
        self.bid = int(bid)

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        for i in range(len(self.cards)):
            if self.cards[i] != other.cards[i]:
                return self.cards[i] < other.cards[i]

    def account_for_jokers(self):
        jokers = self.counted_cards_jokers["J"]
        del self.counted_cards_jokers["J"]
        if len(self.counted_cards_jokers) > 0:
            self.counted_cards_jokers[
                self.counted_cards_jokers.most_common(1)[0][0]
            ] += jokers
        else:  # Edge case: "JJJJJ"
            self.counted_cards_jokers["A"] = jokers

    def get_hand_type(self):
        counted_hand = self.counted_cards_jokers if self.jokers else self.counted_cards
        if len(counted_hand) == 1:
            self.hand_type = 7  # five of a kind
        elif counted_hand.most_common(1)[0][1] == 4:
            self.hand_type = 6  # four of a kind
        elif (
            counted_hand.most_common(2)[0][1] == 3
            and counted_hand.most_common(2)[1][1] == 2
        ):
            self.hand_type = 5  # full house
        elif counted_hand.most_common(1)[0][1] == 3:
            self.hand_type = 4  # three of a kind
        elif (
            counted_hand.most_common(2)[0][1] == 2
            and counted_hand.most_common(2)[1][1] == 2
        ):
            self.hand_type = 3  # two pair
        elif counted_hand.most_common(1)[0][1] == 2:
            self.hand_type = 2  # one pair
        else:
            self.hand_type = 1  # high card


def winnings(lines, jokers=False):
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards, bid, jokers))
    hands = sorted(hands)
    for i, hand in enumerate(hands):
        hand.winnings = hand.bid * (i + 1)
    return sum(hand.winnings for hand in hands)


if __name__ == "__main__":
    lines = load_strs("inputs/day07.txt")
    print(f"Part 1: {winnings(lines)}")
    print(f"Part 2: {winnings(lines, jokers=True)}")


# -- Tests --
fixture = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]


def test_part_1():
    assert winnings(fixture) == 6440


def test_part_2():
    assert winnings(fixture, jokers=True) == 5905
