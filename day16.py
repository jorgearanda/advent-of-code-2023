import sys

from cartography import Map
from loader import load_strs


sys.setrecursionlimit(10_000)


def beam(cell, direction):
    if cell.extra["energy"] is None:
        cell.extra["energy"] = set()
    if direction in cell.extra["energy"]:
        return
    cell.extra["energy"].add(direction)
    if cell.val == "." and cell.neighbours.get(direction) is not None:
        beam(cell.neighbours[direction], direction)
    elif cell.val == "\\":
        if direction == "E" and cell.neighbours.get("S") is not None:
            beam(cell.neighbours["S"], "S")
        elif direction == "S" and cell.neighbours.get("E") is not None:
            beam(cell.neighbours["E"], "E")
        elif direction == "W" and cell.neighbours.get("N") is not None:
            beam(cell.neighbours["N"], "N")
        elif direction == "N" and cell.neighbours.get("W") is not None:
            beam(cell.neighbours["W"], "W")
        return
    elif cell.val == "/":
        if direction == "E" and cell.neighbours.get("N") is not None:
            beam(cell.neighbours["N"], "N")
        elif direction == "N" and cell.neighbours.get("E") is not None:
            beam(cell.neighbours["E"], "E")
        elif direction == "W" and cell.neighbours.get("S") is not None:
            beam(cell.neighbours["S"], "S")
        elif direction == "S" and cell.neighbours.get("W") is not None:
            beam(cell.neighbours["W"], "W")
        return
    elif cell.val == "-":
        if direction in "EW" and cell.neighbours.get(direction) is not None:
            beam(cell.neighbours[direction], direction)
        elif direction in "NS":
            if cell.neighbours.get("W") is not None:
                beam(cell.neighbours["W"], "W")
            if cell.neighbours.get("E") is not None:
                beam(cell.neighbours["E"], "E")
    elif cell.val == "|":
        if direction in "NS" and cell.neighbours.get(direction) is not None:
            beam(cell.neighbours[direction], direction)
        elif direction in "EW":
            if cell.neighbours.get("S") is not None:
                beam(cell.neighbours["S"], "S")
            if cell.neighbours.get("N") is not None:
                beam(cell.neighbours["N"], "N")


def count_energized_cells(grid):
    return sum(cell.extra["energy"] is not None for row in grid.cells for cell in row)


def find_max_energy(lines):
    max_energy = 0
    for j in range(len(lines)):
        m = Map(lines, diag=False, energy=None)
        beam(m.cells[j][0], "E")
        max_energy = max(max_energy, count_energized_cells(m))

        m = Map(lines, diag=False, energy=None)
        beam(m.cells[j][-1], "W")
        max_energy = max(max_energy, count_energized_cells(m))

    for i in range(len(lines[0])):
        m = Map(lines, diag=False, energy=None)
        beam(m.cells[0][i], "S")
        max_energy = max(max_energy, count_energized_cells(m))

        m = Map(lines, diag=False, energy=None)
        beam(m.cells[-1][i], "N")
        max_energy = max(max_energy, count_energized_cells(m))

    return max_energy


if __name__ == "__main__":
    m = Map(load_strs("inputs/day16.txt"), diag=False, energy=None)
    beam(m.cells[0][0], "E")
    print(f"Part 1: {count_energized_cells(m)}")
    print(f"Part 2: {find_max_energy(load_strs('inputs/day16.txt'))}")


# -- Tests --
fixture = [
    ".|...\\....",
    "|.-.\\.....",
    ".....|-...",
    "........|.",
    "..........",
    ".........\\",
    "..../.\\\\..",
    ".-.-/..|..",
    ".|....-|.\\",
    "..//.|....",
]


def test_map_works():
    m = Map(fixture, diag=False, energy=None)
    assert len(m.cells) == 10
    assert all(len(row) == 10 for row in m.cells)
    assert m.cells[0][0].val == "."
    assert m.cells[0][0].extra["energy"] is None


def test_part_1():
    m = Map(fixture, diag=False, energy=None)
    beam(m.cells[0][0], "E")
    assert count_energized_cells(m) == 46


def test_part_2():
    assert find_max_energy(fixture) == 51
