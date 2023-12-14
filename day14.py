from loader import load_strs


def rotate(grid):
    """Ninety degrees clockwise."""
    rotated = [""] * len(grid[0])
    for j in range(len(grid) - 1, -1, -1):
        for i in range(len(grid[j])):
            rotated[i] += grid[j][i]
    return rotated


def tilt(grid):
    grid = rotate(grid)
    tilted = []
    for line in grid:
        i = 0
        tilted_line = ""
        while i < len(line):
            if line[i] == "#":
                tilted_line += "#"
                i += 1
                continue
            try:
                next_cube = line.index("#", i)
            except ValueError:
                next_cube = len(line)
            round_rocks = line.count("O", i, next_cube)
            empty = line.count(".", i, next_cube)
            tilted_line += "." * empty
            tilted_line += "O" * round_rocks
            i += round_rocks + empty
        tilted.append(tilted_line)
    return tilted


def spin(grid):
    for _ in range(4):
        grid = tilt(grid)
    return grid


def total_load(grid):
    tilted = tilt(grid)
    res = 0
    for line in tilted:
        for i, char in enumerate(line):
            res += i + 1 if char == "O" else 0
    return res


def find_load_after_cycle(grid):
    cfgs = {}
    i = 0
    cycle = None
    seen = []
    while True:
        grid = spin(grid)
        i += 1
        tgrid = tuple(grid)
        seen.append(tgrid)
        if tgrid in cfgs:
            cycle = i - cfgs[tgrid]
            break
        cfgs[tuple(grid)] = i
    return get_load(seen[((1_000_000_000 - i) % 7) - cycle - 1])


def get_load(grid):
    rotated = rotate(grid)
    res = 0
    for line in rotated:
        for i, char in enumerate(line):
            res += i + 1 if char == "O" else 0
    return res


if __name__ == "__main__":
    grid = load_strs("inputs/day14.txt")
    print(f"Part 1: {total_load(grid)}")
    print(f"Part 2: {find_load_after_cycle(grid)}")

# -- Tests --
fixture = [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#....",
]


def test_rotate():
    assert rotate(["123", "456", "789"]) == ["741", "852", "963"]


def test_tilt():
    assert tilt(fixture)[2] == "..OO#....O"


def test_part_1():
    assert total_load(fixture) == 136


def test_part_2():
    assert find_load_after_cycle(fixture) == 64
