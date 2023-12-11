from itertools import combinations

from loader import load_strs


def parse(lines, expansion=2):
    galaxies = []
    distances = []
    for j, line in enumerate(lines):
        if "#" in line:
            distances.append([1 for _ in line])
            last_idx = 0
            while True:
                try:
                    last_idx = line.index("#", last_idx)
                except ValueError:
                    break
                galaxies.append((j, last_idx))
                last_idx += 1
        else:
            distances.append([expansion for _ in line])
    for i in range(len(lines[0])):
        if all(cell != "#" for line in lines for cell in line[i]):
            for j in range(len(lines)):
                distances[j][i] *= expansion
    return galaxies, distances


def find_distance(g1, g2, space):
    d = 0
    if g1[0] != g2[0]:
        d += sum(line[g1[1]] for line in space[g1[0] : g2[0]])
    if g1[1] != g2[1]:
        if g1[1] < g2[1]:
            d += sum(space[g2[0]][g1[1] + 1 : g2[1] + 1])
        else:
            d += sum(space[g2[0]][g2[1] : g1[1]])
    return d


def sum_distances(lines, expansion=2):
    galaxies, space = parse(lines, expansion=expansion)
    return sum(
        find_distance(combination[0], combination[1], space)
        for combination in combinations(galaxies, 2)
    )


if __name__ == "__main__":
    lines = load_strs("inputs/day11.txt")
    print(f"Part 1: {sum_distances(lines)}")
    print(f"Part 2: {sum_distances(lines, expansion=1_000_000)}")


# -- Tests --
fixture = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]


def test_find_galaxies():
    galaxies, _ = parse(fixture)
    assert len(galaxies) == 9
    assert galaxies[0] == (0, 3)
    assert galaxies[-1] == (9, 4)


def test_make_distances():
    _, distances = parse(fixture)
    assert distances[0][0] == 1
    assert distances[1][2] == 2
    assert distances[3][5] == 4


def test_find_distance():
    gs, ds = parse(fixture)
    assert find_distance(gs[0], gs[6], ds) == 15
    assert find_distance(gs[1], gs[2], ds) == 10
    assert find_distance(gs[4], gs[8], ds) == 9
    assert find_distance(gs[7], gs[8], ds) == 5


def test_part_1():
    assert sum_distances(fixture) == 374


def test_part_2():
    assert sum_distances(fixture, expansion=100) == 8410
