from itertools import cycle
from math import lcm

from loader import load_strs


def parse(lines):
    return {line[:3]: (line[7:10], line[12:15]) for line in lines}


def follow(lines):
    instructions = lines[0]
    nodes = parse(lines[2:])
    cur_node = "AAA"
    steps = 0
    for instruction in cycle(instructions):
        steps += 1
        cur_node = nodes[cur_node][0 if instruction == "L" else 1]
        if cur_node == "ZZZ":
            break
    return steps


def follow_ghost(lines):
    instructions = lines[0]
    steps_to_z = []
    nodes = parse(lines[2:])
    a_nodes = [node for node in nodes if node.endswith("A")]
    for node in a_nodes:
        cur_node = node
        steps = 0
        for instruction in cycle(instructions):
            steps += 1
            cur_node = nodes[cur_node][0 if instruction == "L" else 1]
            if cur_node.endswith("Z"):
                break
        steps_to_z.append(steps)
    return lcm(*steps_to_z)


if __name__ == "__main__":
    lines = load_strs("inputs/day08.txt")
    print(f"Part 1: {follow(lines)}")
    print(f"Part 2: {follow_ghost(lines)}")


# -- Tests --
fixture1 = [
    "RL",
    "",
    "AAA = (BBB, CCC)",
    "BBB = (DDD, EEE)",
    "CCC = (ZZZ, GGG)",
    "DDD = (DDD, DDD)",
    "EEE = (EEE, EEE)",
    "GGG = (GGG, GGG)",
    "ZZZ = (ZZZ, ZZZ)",
]

fixture2 = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)",
]

fixture3 = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]


def test_part_1():
    assert follow(fixture1) == 2
    assert follow(fixture2) == 6


def test_part_2():
    assert follow_ghost(fixture3) == 6
