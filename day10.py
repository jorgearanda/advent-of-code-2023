from cartography import Map

from loader import load_strs


def find_start(m):
    for row in m.cells:
        for cell in row:
            if cell.val == "S":
                return cell


def initialize(m):
    for row in m.cells:
        for cell in row:
            cell.in_loop = False
            cell.inside = False


def colour_inside(cell, directions):
    changes = 0
    for direction in directions:
        if (
            cell.neighbours.get(direction) is not None
            and not cell.neighbours[direction].in_loop
            and not cell.neighbours[direction].inside
        ):
            cell.neighbours[direction].inside = True
            changes += 1
    return changes


def trace(m):
    steps = 0
    start = find_start(m)
    cell = start
    cell.in_loop = True
    cell.inside = False
    if cell.neighbours.get("S") is not None and cell.neighbours["S"].val in "|LJ":
        direction = "S"
    elif cell.neighbours.get("W") is not None and cell.neighbours["W"].val in "-FL":
        direction = "W"
    else:
        direction = "N"
    while True:
        steps += 1
        cell = cell.neighbours[direction]
        cell.in_loop = True
        cell.inside = False
        if direction == "N":
            if cell.val == "|":
                direction = "N"
                colour_inside(cell, ["NE", "E", "SE"])
            elif cell.val == "7":
                direction = "W"
                colour_inside(cell, ["NE", "E", "N"])
            elif cell.val == "F":
                direction = "E"
                colour_inside(cell, ["SE"])
        elif direction == "E":
            if cell.val == "-":
                direction = "E"
                colour_inside(cell, ["SE", "S", "SW"])
            elif cell.val == "7":
                direction = "S"
                colour_inside(cell, ["SW"])
            elif cell.val == "J":
                direction = "N"
                colour_inside(cell, ["SE", "E", "S"])
        elif direction == "S":
            if cell.val == "|":
                direction = "S"
                colour_inside(cell, ["NW", "W", "SW"])
            elif cell.val == "J":
                direction = "W"
                colour_inside(cell, ["NW"])
            elif cell.val == "L":
                direction = "E"
                colour_inside(cell, ["SW", "W", "S"])
        elif direction == "W":
            if cell.val == "-":
                direction = "W"
                colour_inside(cell, ["NE", "N", "NW"])
            elif cell.val == "F":
                direction = "S"
                colour_inside(cell, ["NW", "W", "N"])
            elif cell.val == "L":
                direction = "N"
                colour_inside(cell, ["NE"])
        if cell == start:
            break
    return int(steps / 2)


def fill(m):
    done = False
    while not done:
        done = True
        for row in m.cells:
            for cell in row:
                if cell.inside:
                    changes = colour_inside(
                        cell, ["NW", "N", "NE", "W", "E", "SW", "S", "SE"]
                    )
                    if changes > 0:
                        done = False


def sum_inside(m):
    return sum(cell.inside for row in m.cells for cell in row)


def print_loop(m):
    for row in m.cells:
        r = ""
        for cell in row:
            if cell.in_loop:
                r += cell.val
            elif cell.inside:
                r += "."
            else:
                r += "@"
        print(r)


if __name__ == "__main__":
    m = Map(load_strs("inputs/day10.txt"), diag=True)
    initialize(m)
    print(f"Part 1: {trace(m)}")
    fill(m)
    print(f"Part 2: {sum_inside(m)}")


# -- Tests --
fixture1 = [
    ".....",
    ".S-7.",
    ".|.|.",
    ".L-J.",
    ".....",
]

fixture2 = [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ...",
]

fixture3 = [
    ".F----7F7F7F7F-7....",
    ".|F--7||||||||FJ....",
    ".||.FJ||||||||L7....",
    "FJL7L7LJLJ||LJ.L-7..",
    "L--J.L7...LJS7F-7L7.",
    "....F-J..F7FJ|L7L7L7",
    "....L7.F7||L7|.L7L7|",
    ".....|FJLJ|FJ|F7|.LJ",
    "....FJL-7.||.||||...",
    "....L---J.LJ.LJLJ...",
]


def test_find_start():
    m = Map(fixture1)
    initialize(m)
    assert find_start(m).val == "S"


def test_part_1():
    m = Map(fixture1)
    initialize(m)
    assert trace(m) == 4

    m2 = Map(fixture2)
    initialize(m2)
    assert trace(m2) == 8


def test_part_2():
    m3 = Map(fixture3)
    initialize(m3)
    trace(m3)
    fill(m3)
    assert sum_inside(m3) == 8
