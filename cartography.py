class Cell:
    def __init__(self, i, j, val, **kwargs):
        self.i = i
        self.j = j
        self.val = val
        self.extra = {}
        for key in kwargs:
            self.extra[key] = kwargs[key]
        self.neighbours = {}

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return f"Cell({self.i}, {self.j}): {self.val}"


class Map:
    def __init__(self, lines, diag=False, **kwargs):
        self.cells = []
        self.cells.extend(
            [Cell(i, j, val, **kwargs) for i, val in enumerate(line)]
            for j, line in enumerate(lines)
        )
        self.set_neighbours(diag)

    def __str__(self):
        res = ""
        for row in self.cells:
            for cell in row:
                res += str(cell.val)
            res += "\n"
        return res

    def set_neighbours(self, diag=False):
        for j in range(len(self.cells)):
            for i in range(len(self.cells[0])):
                if j > 0:
                    self.cells[j][i].neighbours["N"] = self.cells[j - 1][i]
                if diag:
                    if i > 0:
                        self.cells[j][i].neighbours["NW"] = self.cells[j - 1][i - 1]
                    if i < len(self.cells[j - 1]) - 1:
                        self.cells[j][i].neighbours["NE"] = self.cells[j - 1][i + 1]
                if i > 0:
                    self.cells[j][i].neighbours["W"] = self.cells[j][i - 1]
                if i < len(self.cells[j]) - 1:
                    self.cells[j][i].neighbours["E"] = self.cells[j][i + 1]
                if j < len(self.cells) - 1:
                    self.cells[j][i].neighbours["S"] = self.cells[j + 1][i]
                    if diag:
                        if i > 0:
                            self.cells[j][i].neighbours["SW"] = self.cells[j + 1][i - 1]
                        if i < len(self.cells[j + 1]) - 1:
                            self.cells[j][i].neighbours["SE"] = self.cells[j + 1][i + 1]


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


def test_map_init():
    m = Map(fixture)
    assert len(m.cells) == 10
    assert str(m).startswith(fixture[0])
    assert m.cells[0][0].val == "4"
    assert m.cells[1][3].val == "*"


def test_map_neighbours():
    m = Map(fixture)
    assert len(m.cells[0][0].neighbours) == 2
    assert m.cells[0][0].neighbours["E"] == m.cells[0][1]
    assert m.cells[0][0].neighbours["S"] == m.cells[1][0]


def test_map_neighbours_diag():
    m = Map(fixture, diag=True)
    assert len(m.cells[1][1].neighbours) == 8
    assert m.cells[1][1].neighbours["NW"] == m.cells[0][0]
    assert m.cells[1][1].neighbours["SE"] == m.cells[2][2]
