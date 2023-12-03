from collections import defaultdict

from loader import load_strs


class Cell:
    def __init__(self, i, j, val):
        self.i = i
        self.j = j
        self.val = val


def find_parts_and_gears(schematic):
    parts = []
    gears = defaultdict(list)
    for j in range(len(schematic)):
        row = schematic[j]
        part = ""
        scanning_part = False
        symbol_adj = False
        gear_coords = None
        for i in range(len(row)):
            if row[i].isdigit():
                scanning_part = True
                part += row[i]
                symbol_adj = symbol_adj or is_symbol_adj(i, j, schematic)
                adj_gear = get_adjacent_gear(i, j, schematic)
                if adj_gear is not None:
                    gear_coords = adj_gear
            else:
                if scanning_part and symbol_adj:
                    parts.append(int(part))
                if scanning_part and gear_coords:
                    gears[gear_coords].append(int(part))
                scanning_part = False
                part = ""
                symbol_adj = False
                gear_coords = None
        if scanning_part and symbol_adj:
            parts.append(int(part))
        if scanning_part and gear_coords:
            gears[gear_coords].append(int(part))
    return parts, gears


def is_symbol_adj(i, j, schematic):
    return any(
        not cell.val.isdigit() and cell.val != "."
        for cell in get_adjacent_cells(i, j, schematic)
    )


def get_adjacent_gear(i, j, schematic):
    cells = get_adjacent_cells(i, j, schematic)
    for cell in cells:
        if cell.val == "*":
            return (cell.i, cell.j)


def get_adjacent_cells(i, j, schematic):
    adj_cells = []
    if j > 0:
        adj_cells.append(Cell(i, j - 1, schematic[j - 1][i]))
        if i > 0:
            adj_cells.append(Cell(i - 1, j - 1, schematic[j - 1][i - 1]))
        if i < len(schematic[j - 1]) - 1:
            adj_cells.append(Cell(i + 1, j - 1, schematic[j - 1][i + 1]))
    if i > 0:
        adj_cells.append(Cell(i - 1, j, schematic[j][i - 1]))
    if i < len(schematic[j]) - 1:
        adj_cells.append(Cell(i + 1, j, schematic[j][i + 1]))
    if j < len(schematic) - 1:
        adj_cells.append(Cell(i, j + 1, schematic[j + 1][i]))
        if i > 0:
            adj_cells.append(Cell(i - 1, j + 1, schematic[j + 1][i - 1]))
        if i < len(schematic[j + 1]) - 1:
            adj_cells.append(Cell(i + 1, j + 1, schematic[j + 1][i + 1]))
    return adj_cells


def sum_part_numbers(parts):
    return sum(parts)


def sum_gear_ratios(gears):
    return sum(gear[0] * gear[1] for gear in gears.values() if len(gear) == 2)


if __name__ == "__main__":
    parts, gears = find_parts_and_gears(load_strs("inputs/day03.txt"))
    print(f"Part 1: {sum_part_numbers(parts)}")
    print(f"Part 2: {sum_gear_ratios(gears)}")


# -- Tests --
fixture = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


def test_part_1():
    parts, _ = find_parts_and_gears(fixture)
    assert sum_part_numbers(parts) == 4361


def test_part_2():
    _, gears = find_parts_and_gears(fixture)
    assert sum_gear_ratios(gears) == 467835
