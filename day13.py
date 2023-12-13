from copy import deepcopy

from loader import load_strs


def find_reflection(pattern, refuse=0):
    for i in range(1, len(pattern)):
        if i == refuse:
            continue
        smaller_len = min(i, len(pattern) - i)
        if list(reversed(pattern[i - smaller_len : i])) == pattern[i : i + smaller_len]:
            return i
    return 0


def get_patterns(lines):
    patterns = []
    pattern = []
    for line in lines:
        if len(line) == 0:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)
    return patterns


def transpose(pattern):
    transposed = [""] * len(pattern[0])
    for j in range(len(pattern)):
        for i in range(len(pattern[j])):
            transposed[i] += pattern[j][i]
    return transposed


def summarize(lines):
    patterns = get_patterns(lines)
    total = 0
    for pattern in patterns:
        total += 100 * find_reflection(pattern)
        total += find_reflection(transpose(pattern))
    return total


def look_for_smudge(pattern):
    orig_pattern = deepcopy(pattern)
    orig_transpose = transpose(pattern)
    orig_horizontal = find_reflection(pattern)
    orig_vertical = find_reflection(transpose(pattern))
    for j in range(len(pattern)):
        for i in range(len(pattern[0])):
            pattern = deepcopy(orig_pattern)
            transposed = deepcopy(orig_transpose)
            if pattern[j][i] == "#":
                pattern[j] = f"{pattern[j][:i]}.{pattern[j][i + 1:]}"
                transposed[i] = f"{transposed[i][:j]}.{transposed[i][j + 1:]}"
            else:
                pattern[j] = f"{pattern[j][:i]}#{pattern[j][i + 1:]}"
                transposed[i] = f"{transposed[i][:j]}#{transposed[i][j + 1:]}"
            horizontal = find_reflection(pattern, refuse=orig_horizontal)
            if horizontal != 0:
                return 100 * horizontal
            vertical = find_reflection(transposed, refuse=orig_vertical)
            if vertical != 0:
                return vertical


def summarize_with_smudges(lines):
    patterns = get_patterns(lines)
    return sum(look_for_smudge(pattern) for pattern in patterns)


if __name__ == "__main__":
    lines = load_strs("inputs/day13.txt")
    print(f"Part 1: {summarize(lines)}")
    print(f"Part 2: {summarize_with_smudges(lines)}")


# -- Tests --
fixture = [
    "#.##..##.",
    "..#.##.#.",
    "##......#",
    "##......#",
    "..#.##.#.",
    "..##..##.",
    "#.#.##.#.",
    "",
    "#...##..#",
    "#....#..#",
    "..##..###",
    "#####.##.",
    "#####.##.",
    "..##..###",
    "#....#..#",
]


def test_get_patterns():
    patterns = get_patterns(fixture)
    assert len(patterns) == 2
    assert len(patterns[1]) == 7
    assert patterns[0][6] == "#.#.##.#."


def test_find_reflection():
    patterns = get_patterns(fixture)
    assert find_reflection(patterns[0]) == 0
    assert find_reflection(patterns[1]) == 4


def test_part_1():
    assert summarize(fixture) == 405


def test_part_2():
    assert summarize_with_smudges(fixture) == 400
