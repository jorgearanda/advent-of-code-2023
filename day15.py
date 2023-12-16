import contextlib
from collections import defaultdict

from loader import load_strs


def hash(code):
    res = 0
    for char in code:
        res += ord(char)
        res *= 17
        res %= 256
    return res


def sum_hashes(sequence):
    return sum(hash(code) for code in sequence.split(","))


def get_boxes_hashmap(sequence):
    boxes = defaultdict(dict)
    for code in sequence.split(","):
        if "=" in code:
            label, focal_length = code.split("=")
            boxes[hash(label)][label] = int(focal_length)
        else:
            label = code[:-1]
            with contextlib.suppress(KeyError):
                del boxes[hash(label)][label]
    return boxes


def get_power(sequence):
    boxes = get_boxes_hashmap(sequence)
    res = 0
    for num, lenses in boxes.items():
        for position, val in enumerate(lenses.values(), start=1):
            res += (num + 1) * position * val
    return res


if __name__ == "__main__":
    sequence = load_strs("inputs/day15.txt")[0]
    print(f"Part 1: {sum_hashes(sequence)}")
    print(f"Part 2: {get_power(sequence)}")


# -- Tests --
fixture = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_hash():
    assert hash("HASH") == 52


def test_part_1():
    assert sum_hashes(fixture) == 1320


def test_part_2():
    assert get_power(fixture) == 145
