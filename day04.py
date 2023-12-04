from collections import defaultdict

from loader import load_strs


def winning_numbers(card):
    nums = card.split(": ")[1]
    winners, selected = nums.split(" | ")
    winners = set(winners.split())
    selected = set(selected.split())
    return len(winners & selected)


def points(card):
    winners = winning_numbers(card)
    return 0 if winners == 0 else 2 ** (winners - 1)


def sum_points(cards):
    return sum(points(card) for card in cards)


def card_id(card):
    return int(card.split(":")[0].split()[1])


def copies(cards):
    res = defaultdict(int)
    for card in cards:
        cid = card_id(card)
        res[cid] += 1
        for i in range(winning_numbers(card)):
            res[cid + 1 + i] += res[cid]
    return sum(res.values())


if __name__ == "__main__":
    cards = load_strs("inputs/day04.txt")
    print(f"Part 1: {sum_points(cards)}")
    print(f"Part 2: {copies(cards)}")


# -- Tests --
fixture = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


def test_part_1():
    assert sum_points(fixture) == 13


def test_card_id():
    assert card_id(fixture[0]) == 1


def test_part_2():
    assert copies(fixture) == 30
